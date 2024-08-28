# python/tools/web_scraper.py

import requests
from bs4 import BeautifulSoup
from python.helpers.tool import Tool, Response
from python.helpers import files
from python.helpers.print_style import PrintStyle

class WebScraper(Tool):

    def execute(self, url="", element="", attribute="", **kwargs):
        try:
            # Send an HTTP GET request to the specified URL
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract elements based on the provided tag or class
            if element:
                result = soup.find_all(element)
            elif attribute:
                result = soup.find_all(attrs={attribute.split('=')[0]: attribute.split('=')[1]})

            # Format the result
            extracted_texts = [str(res) for res in result]
            formatted_result = "\n\n".join(extracted_texts)

            if not formatted_result:
                formatted_result = "No elements found."

            return Response(message=formatted_result, break_loop=False)

        except requests.RequestException as e:
            return Response(message=f"Error fetching the page: {e}", break_loop=True)
        except Exception as e:
            return Response(message=f"Error processing the page: {e}", break_loop=True)

    def before_execution(self, **kwargs):
        PrintStyle(font_color="#1B4F72", padding=True, background_color="white", bold=True).print(f"{self.agent.agent_name}: Starting web scraping...")

    def after_execution(self, response, **kwargs):
        msg_response = files.read_file("./prompts/fw.tool_response.md", tool_name=self.name, tool_response=response.message)
        self.agent.append_message(msg_response, human=True)
        PrintStyle(font_color="#1B4F72", background_color="white", padding=True, bold=True).print(f"{self.agent.agent_name}: Response from web scraping:")
        PrintStyle(font_color="#85C1E9").print(response.message)
