import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def scrape_table(url):
    # Send a GET request to the URL
    req_headers = {
        "Host": "intrauam.autonoma.edu.co",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://intrauam.autonoma.edu.co/intrauam2/l/url/estudiantes/horario/dobleCarrera.php",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "28",
        "Origin": "https://intrauam.autonoma.edu.co",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=m6qtkjsltpugastiacc2ng4i70",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
    }
    response = requests.post(
        url, data={"plan": "1020", "usuario": "1054478436"}, headers=req_headers
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        print("Content: ", response.content)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the first table on the page
        table = soup.find("table", class_="datos")

        # Initialize a list to hold the table data
        data = []

        # Extract headers
        headers = []
        for th in table.find_all("th"):
            headers.append(th.text.strip())

        # Extract rows
        for row in table.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        return headers, data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None, None


def main():
    url = "https://intrauam.autonoma.edu.co/intrauam2/l/url/docente/horarioAsignatura/editar_sel.php?letra=A&periodo=1&ano=2025"  # Example URL
    headers, table_data = scrape_table(url)

    if table_data:
        # Print the DataFrame in a tabulated format
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
