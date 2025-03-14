import pytest
from bilix.dm import dm2json, dm2ass_factory
from bilix.download import DownloaderBilibili


@pytest.mark.asyncio
async def test_choose_quality():
    import os
    from bilix.download.downloader_bilibili import choose_quality
    import bilix.api.bilibili as api
    from httpx import AsyncClient

    client = AsyncClient(headers={'user-agent': 'PostmanRuntime/7.29.0', 'referer': 'https://www.bilibili.com'},
                         cookies={'SESSDATA': os.getenv('BILI_TOKEN')}, http2=True)
    # dolby
    data = await api.get_video_info(client, "https://www.bilibili.com/video/BV13L4y1K7th")
    try:
        video_info, audio_info = choose_quality(data.dash, data.support_formats, quality=999, codec=":ec-3")
    except ValueError:
        assert not os.getenv("BILI_TOKEN")
    # normal
    choose_quality(data.dash, data.support_formats, quality="720P", codec="hev")
    # hi-res
    data = await api.get_video_info(client, "https://www.bilibili.com/video/BV16K411S7sk")
    try:
        video_info, audio_info = choose_quality(data.dash, data.support_formats,
                                                quality='1080P', codec="hev:fLaC")
    except ValueError:
        assert not os.getenv("BILI_TOKEN")
    await client.aclose()


@pytest.mark.asyncio
async def test_get_collect_or_list():
    d = DownloaderBilibili()
    await d.get_collect_or_list('https://space.bilibili.com/54296062/channel/collectiondetail?sid=412818&ctype=0',
                                quality=999)
    await d.get_collect_or_list('https://space.bilibili.com/8251621/channel/seriesdetail?sid=2323334&ctype=0',
                                quality=999)
    await d.aclose()


@pytest.mark.asyncio
async def test_get_favour():
    d = DownloaderBilibili()
    await d.get_favour("69072721", num=1, quality=999)
    await d.aclose()


@pytest.mark.asyncio
async def test_get_cate():
    d = DownloaderBilibili()
    await d.get_cate_videos("宅舞", keyword="jk", order="click", num=1, quality=1)
    await d.aclose()


@pytest.mark.asyncio
async def test_get_up():
    d = DownloaderBilibili()
    await d.get_up_videos("455511061", order="pubdate", num=1, quality=1)
    await d.aclose()


@pytest.mark.asyncio
async def test_get_series():
    d = DownloaderBilibili()
    await d.get_series("https://www.bilibili.com/video/BV1jK4y1N7ST?p=3", p_range=(5, 5), quality=999)
    # only audio
    await d.get_series("https://www.bilibili.com/video/BV1jK4y1N7ST?p=3", p_range=(5, 5), only_audio=True)
    # hierarchy False
    await d.get_series("https://www.bilibili.com/video/BV1jK4y1N7ST?p=3", p_range=(1, 1),
                       hierarchy=False, image=True, quality=999)
    # 单个视频
    await d.get_series("https://www.bilibili.com/video/BV1sS4y1b7qb?spm_id_from=333.999.0.0", quality=999)
    await d.aclose()


@pytest.mark.asyncio
async def test_get_dm():
    d = DownloaderBilibili()
    await d.get_dm('https://www.bilibili.com/video/BV11Z4y1z7s8?spm_id_from=333.337.search-card.all.click')
    await d.get_dm('https://www.bilibili.com/video/BV11Z4y1z7s8?spm_id_from=333.337.search-card.all.click',
                   convert_func=dm2json)
    await d.get_dm('https://www.bilibili.com/video/BV11Z4y1z7s8?spm_id_from=333.337.search-card.all.click',
                   convert_func=dm2ass_factory(1920, 1080))
    await d.aclose()


@pytest.mark.asyncio
async def test_get_subtitle():
    d = DownloaderBilibili()
    await d.get_subtitle("https://www.bilibili.com/video/BV1hS4y1m7Ma")
    await d.aclose()
