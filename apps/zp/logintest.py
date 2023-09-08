import requests


class ZwiftLogin(object):
    def __init__(self, login_data=None):
        if login_data is None:
            try:
                self.login_data = {"username": "", "password": "", "login": "Login"}
            except Exception as e:
                print("login_data: Need a proper config.ini file or supply login info")
                raise e
        else:
            self.login_data = login_data

    def get_request(self, viewurl, content=False):
        with requests.Session() as session:  # Use 'requests.Session()' instead of 'HTMLSession()'
            response_initial = session.get("https://zwiftpower.com")
            print(session.cookies)
            self.login_data["sid"] = session.cookies.get("phpbb3_lswlk_sid")

            if "Login Required" in response_initial.text:
                try:
                    session.post("https://www.zwiftpower.com/ucp.php?mode=login", data=self.login_data)
                    response_check = session.get("https://zwiftpower.com/events.php")
                    assert "Profile" in response_check.text
                    print("Login successful")
                except Exception as e:
                    print("Login error")
                    print(f"Failed to login: {e}")
            response_initial = session.get("https://zwiftpower.com")
            print(response_initial.cookies)
            # You might want to ensure that necessary CloudFront cookies are in your session
            # assert session.cookies.get("CloudFront-Policy") is not None
            # assert session.cookies.get("CloudFront-Signature") is not None
            # assert session.cookies.get("CloudFront-Key-Pair-Id") is not None

            response = session.get(viewurl)

            print("Status", response.status_code)
            if content:
                return response.content
            else:
                return response.json()


# Example Usage
zp = ZwiftLogin({"username": "karthick", "password": "X8XeFyb8t4Xrk$K"})
data = zp.get_request("https://zwiftpower.com/cache3/results/3775984_zwift.json")
print(data)
