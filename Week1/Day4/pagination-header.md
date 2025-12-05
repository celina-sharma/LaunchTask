### Navigating Pages

Page 1 was fetched using:
curl -I "https://api.github.com/users/octocat/repos?page=1&per_page=5"

The Link header returned:

<https://api.github.com/user/583231/repos?page=2&per_page=5>; rel="next",
<https://api.github.com/user/583231/repos?page=2&per_page=5>; rel="last"


Pge 2 was fetched using:
curl -I "https://api.github.com/user/583231/repos?page=2&per_page=5"

The link header returned:
<https://api.github.com/user/583231/repos?page=1&per_page=5>; rel="prev" 
<https://api.github.com/user/583231/repos?page=1&per_page=5>; rel="first"