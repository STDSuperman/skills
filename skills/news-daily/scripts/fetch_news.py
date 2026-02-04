import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from bs4 import BeautifulSoup
import re


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

TIMEOUT = 10
RETRIES = 3


@dataclass
class NewsItem:
    title: str
    url: str
    platform: str
    platform_icon: str
    raw_category: str
    content: str = ""
    timestamp: datetime = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.timestamp:
            data["timestamp"] = self.timestamp.isoformat()
        return data


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch(url: str, params: dict = None) -> Any:
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        try:
            return response.json()
        except:
            return response.text
    except Exception as e:
        raise Exception(f"Failed to fetch {url}: {str(e)}")


def strip_html(text: str) -> str:
    """Remove HTML tags and clean up text"""
    if not text:
        return ""
    soup = BeautifulSoup(text, "lxml")
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def load_config() -> Dict[str, Any]:
    config_path = os.path.join(os.path.dirname(__file__), "../config/sources.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


class NewsSource:
    def __init__(self, platform: str, config: Dict[str, Any]):
        self.platform = platform
        self.name = config["name"]
        self.icon = config["icon"]
        self.type = config["type"]
        self.category = config["category"]
        self.enabled = config.get("enabled", True)

    def fetch(self) -> List[NewsItem]:
        if not self.enabled:
            return []

        if self.type == "api":
            return self._fetch_api()
        elif self.type == "html":
            return self._fetch_html()
        return []

    def _fetch_api(self) -> List[NewsItem]:
        pass

    def _fetch_html(self) -> List[NewsItem]:
        pass


class ZhihuSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("zhihu", config)
        self.url = config["url"]

    def _fetch_api(self) -> List[NewsItem]:
        data = fetch(self.url)
        items = []
        if "data" in data:
            for item in data["data"]:
                target = item.get("target", {})
                title = target.get("title_area", {}).get("text", "")
                if not title:
                    continue
                url = target.get("url", "")
                content = target.get("excerpt_area", {}).get("text", "")
                items.append(NewsItem(
                    title=title,
                    url=url,
                    platform=self.platform,
                    platform_icon=self.icon,
                    raw_category=self.category,
                    content=content,
                    timestamp=datetime.now()
                ))
        return items


class WallStreetCNSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("wallstreetcn", config)
        self.endpoints = config["endpoints"]

    def _fetch_api(self) -> List[NewsItem]:
        items = []

        for endpoint_key, endpoint_config in self.endpoints.items():
            url = endpoint_config["url"]
            params = endpoint_config.get("params", {})

            try:
                data = fetch(url, params)
                items.extend(self._parse_endpoint(endpoint_key, data))
            except Exception as e:
                print(f"Failed to fetch {endpoint_key}: {str(e)}")

        return items

    def _parse_endpoint(self, endpoint_key: str, data: Any) -> List[NewsItem]:
        items = []

        if "data" not in data or "items" not in data["data"]:
            return items

        if endpoint_key == "live":
            for item in data["data"]["items"]:
                content = item.get("content", "")
                if not content:
                    continue
                content = strip_html(content)
                if not content:
                    continue
                items.append(NewsItem(
                    title=content,
                    url="",
                    platform=self.platform,
                    platform_icon=self.icon,
                    raw_category=self.category,
                    timestamp=datetime.now()
                ))

        elif endpoint_key == "news":
            for item in data["data"]["items"]:
                article = item.get("article")
                if not article:
                    continue
                title = article.get("title", "")
                if not title:
                    continue
                items.append(NewsItem(
                    title=title,
                    url=article.get("uri", ""),
                    platform=self.platform,
                    platform_icon=self.icon,
                    raw_category=self.category,
                    timestamp=datetime.now()
                ))

        elif endpoint_key == "hot":
            for item in data["data"]["items"]:
                article = item.get("article")
                if not article:
                    continue
                title = article.get("title", "")
                if not title:
                    continue
                items.append(NewsItem(
                    title=title,
                    url=article.get("uri", ""),
                    platform=self.platform,
                    platform_icon=self.icon,
                    raw_category=self.category,
                    timestamp=datetime.now()
                ))

        return items


class HupuSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("hupu", config)
        self.url = config["url"]

    def _fetch_html(self) -> List[NewsItem]:
        html = fetch(self.url)
        items = []
        soup = BeautifulSoup(html, "lxml")

        for li in soup.select("li.bbs-sl-web-post-body"):
            a_tag = li.select_one("a.p-title")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            if not title:
                continue
            url = a_tag.get("href", "")
            if url and not url.startswith("http"):
                url = f"https://bbs.hupu.com{url}"
            items.append(NewsItem(
                title=title,
                url=url,
                platform=self.platform,
                platform_icon=self.icon,
                raw_category=self.category,
                timestamp=datetime.now()
            ))

        return items


class ThePaperSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("thepaper", config)
        self.url = config["url"]

    def _fetch_api(self) -> List[NewsItem]:
        data = fetch(self.url)
        items = []

        if "data" in data:
            for item in data["data"]["hotNews"]:
                title = item.get("name", "")
                if not title:
                    continue
                cont_id = item.get("contId", "")
                items.append(NewsItem(
                    title=title,
                    url=f"https://www.thepaper.cn/newsDetail_forward_{cont_id}" if cont_id else "",
                    platform=self.platform,
                    platform_icon=self.icon,
                    raw_category=self.category,
                    timestamp=datetime.now()
                ))

        return items


class HackerNewsSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("hackernews", config)
        self.url = config["url"]

    def _fetch_html(self) -> List[NewsItem]:
        html = fetch(self.url)
        items = []
        soup = BeautifulSoup(html, "lxml")

        for tr in soup.select("tr.athing"):
            title_cell = tr.select_one("td.title span.titleline a")
            if not title_cell:
                continue
            title = title_cell.get_text(strip=True)
            url = title_cell.get("href", "")
            if not title:
                continue
            items.append(NewsItem(
                title=title,
                url=url,
                platform=self.platform,
                platform_icon=self.icon,
                raw_category=self.category,
                timestamp=datetime.now()
            ))

        return items


class ProductHuntSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("producthunt", config)
        self.url = config["url"]

    def _fetch_html(self) -> List[NewsItem]:
        html = fetch(self.url)
        items = []
        soup = BeautifulSoup(html, "lxml")

        for post in soup.select("[data-test^='post-item']"):
            title_elem = post.find(attrs={"data-test": lambda x: x and x.startswith("post-name")})
            if not title_elem:
                continue
            title = title_elem.get_text(strip=True)
            if not title:
                continue
            link_elem = post.select_one("a[href^='/posts/']")
            url = f"https://www.producthunt.com{link_elem.get('href', '')}" if link_elem else ""
            items.append(NewsItem(
                title=title,
                url=url,
                platform=self.platform,
                platform_icon=self.icon,
                raw_category=self.category,
                timestamp=datetime.now()
            ))

        return items


class GitHubSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("github", config)
        self.url = config["url"]

    def _fetch_html(self) -> List[NewsItem]:
        html = fetch(self.url)
        items = []
        soup = BeautifulSoup(html, "lxml")

        for article in soup.select("main .Box div[data-hpc] > article"):
            a_tag = article.select_one("h2 a")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True).replace("\n", "").strip()
            if not title:
                continue
            url = a_tag.get("href", "")
            if url and not url.startswith("http"):
                url = f"https://github.com{url}"
            items.append(NewsItem(
                title=title,
                url=url,
                platform=self.platform,
                platform_icon=self.icon,
                raw_category=self.category,
                timestamp=datetime.now()
            ))

        return items


class SspaiSource(NewsSource):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("sspai", config)
        self.url = config["url"]
        self.params = config.get("params", {})

    def _fetch_api(self) -> List[NewsItem]:
        params = self.params.copy()
        params["created_at"] = int(datetime.now().timestamp())
        data = fetch(self.url, params)
        items = []

        if "data" in data:
            for item in data["data"]:
                title = item.get("title", "")
                if not title:
                    continue
                items.append(NewsItem(
                    title=title,
                    url=item.get("id", ""),
                    platform=self.platform,
                    platform_icon=self.icon,
                    raw_category=self.category,
                    content=item.get("summary", ""),
                    timestamp=datetime.now()
                ))

        return items


SOURCE_MAP = {
    "zhihu": ZhihuSource,
    "wallstreetcn": WallStreetCNSource,
    "hupu": HupuSource,
    "thepaper": ThePaperSource,
    "hackernews": HackerNewsSource,
    "producthunt": ProductHuntSource,
    "github": GitHubSource,
    "sspai": SspaiSource,
}


def fetch_all_news() -> List[NewsItem]:
    config = load_config()
    all_items = []

    for platform_id, platform_config in config["platforms"].items():
        if not platform_config.get("enabled", True):
            continue

        source_class = SOURCE_MAP.get(platform_id)
        if not source_class:
            print(f"Unknown platform: {platform_id}")
            continue

        try:
            source = source_class(platform_config)
            items = source.fetch()
            print(f"{platform_id}: fetched {len(items)} items")
            all_items.extend(items)
        except Exception as e:
            print(f"Error fetching from {platform_id}: {str(e)}")

    return all_items


def main():
    print("📰 开始抓取新闻...")

    items = fetch_all_news()

    print(f"✅ 抓取完成，共 {len(items)} 条新闻")

    output = {
        "total": len(items),
        "items": []
    }

    for item in items:
        output["items"].append({
            "title": item.title,
            "url": item.url,
            "platform": item.platform,
            "platform_icon": item.platform_icon,
            "content": item.content
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
