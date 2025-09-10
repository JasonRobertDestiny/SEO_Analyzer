"""
Async HTTP client for web scraping
"""
import aiohttp
import asyncio
from urllib.parse import urlsplit
import socket
from typing import Optional, Dict, Any


class AsyncHttpClient:
    """Asynchronous HTTP client for web scraping"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    async def __aenter__(self):
        """Create session when entering context"""
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={"User-Agent": self.user_agent}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting context"""
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make GET request with retry logic
        
        Args:
            url: URL to fetch
            **kwargs: Additional arguments for request
            
        Returns:
            Dictionary with 'content', 'status_code', 'headers' or None if failed
        """
        if not self.session:
            raise RuntimeError("HttpClient must be used within async context manager")
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                async with self.session.get(url, **kwargs) as response:
                    content = await response.text()
                    return {
                        'content': content,
                        'status_code': response.status,
                        'headers': dict(response.headers),
                        'url': str(response.url)
                    }
                    
            except asyncio.TimeoutError:
                last_error = f"Timeout fetching {url}"
                await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
                
            except aiohttp.ClientError as e:
                last_error = f"Client error fetching {url}: {str(e)}"
                await asyncio.sleep(1 * (attempt + 1))
                
            except Exception as e:
                last_error = f"Unexpected error fetching {url}: {str(e)}"
                await asyncio.sleep(1 * (attempt + 1))
        
        # All attempts failed
        print(f"Failed to fetch {url} after {self.max_retries} attempts: {last_error}")
        return None
    
    async def head(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make HEAD request"""
        if not self.session:
            raise RuntimeError("HttpClient must be used within async context manager")
        
        try:
            async with self.session.head(url, **kwargs) as response:
                return {
                    'status_code': response.status,
                    'headers': dict(response.headers),
                    'url': str(response.url)
                }
        except Exception as e:
            print(f"HEAD request failed for {url}: {str(e)}")
            return None
    
    async def check_dns(self, url: str) -> bool:
        """Check if DNS resolves for URL"""
        try:
            o = urlsplit(url)
            if not o.hostname:
                return False
            
            # Get event loop for this thread
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, socket.gethostbyname, o.hostname)
            return True
            
        except (socket.herror, socket.gaierror):
            return False
    
    async def get_content_type(self, url: str) -> Optional[str]:
        """Get content type from HEAD request"""
        result = await self.head(url)
        if result:
            return result['headers'].get('content-type', '').split(';')[0]
        return None


# Global instance for direct import
http_client = AsyncHttpClient()