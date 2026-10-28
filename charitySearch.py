import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API_URL = "https://api.charitycommission.gov.uk/register/api/allcharitydetails"

def main():
    registered_number = input("Enter charity number: ").strip()
    suffix = "0"
    api_key = os.getenv("CHARITY_COMMISSION_API_KEY")

    if not registered_number:
        print("A charity number is required.")
        return

    if not api_key:
        print("Set the CHARITY_COMMISSION_API_KEY environment variable first.")
        return

    url = (
        f"{API_URL}/{quote(registered_number, safe='')}/"
        f"{quote(suffix, safe='')}"
    )
    request = Request(url, headers={"Ocp-Apim-Subscription-Key": api_key})

    try:
        with urlopen(request, timeout=15) as response:
            charity = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        print(f"API request failed with HTTP {error.code}: {error.reason}")
        return
    except URLError as error:
        print(f"Could not connect to the Charity Commission API: {error.reason}")
        return
    except json.JSONDecodeError:
        print("The API returned a response that was not valid JSON.")
        return

    print(json.dumps(charity, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()