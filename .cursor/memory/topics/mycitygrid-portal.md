# mycitygrid.com portal recon (no credentials)

Read-only recon, 2026-09-09. No login attempted. Nearly every fact below is a quoted string from the public SPA bundle
`https://www.mycitygrid.com/main.376ce4ebbf71e176.js` (4.5 MB, minified); its hash changes on redeploy, so re-derive it
from the script tags in `/home` if a quote stops matching.

## What we know

- `GET https://www.mycitygrid.com/home` -> `200`, `text/html`, 79579 bytes, and a static file rather than rendered
  output: `Server: Microsoft-IIS/8.5`, `X-Powered-By: ASP.NET`, `ETag`, `Last-Modified`, no `Set-Cookie`.
- It is a **JavaScript app shell**, not server-rendered: the body is `<fuse-splash-screen>` plus `<fuse-root></fuse-root>`
  and three module scripts (`runtime.*.js`, `polyfills.*.js`, `main.*.js`). Angular on the Fuse admin template,
  `<meta name="author" content="Quickode Ltd.">`. No consumption HTML exists without executing JS. `runtime.*.js`
  declares no lazy chunks, so the whole app is in `main.*.js` (webpack chunk `webpackChunkfuse`).
- Client routes (`path:"..."` literals): `login`, `home`, `setpassword`, `initialWindow`, `meters`, `sites`, `users`,
  `reports`, `alerts`, `tickets`, `tariffs`, `readers`, `noga-managment`, plus `:meterId/dashboard`,
  `:meterId/readingLog`, `:userId/dashboard/:addressId/:meterId`; fallback `{path:"**",redirectTo:""}`.
- **API base URL**: an Angular interceptor rewrites every request as `url:"https://www.mycitygrid.com/api/api/"+e.url`
  and, when authenticated, adds `headers.set("Authorization",` `` `Bearer ${o.access_token}` `` `)`.
- `GET https://www.mycitygrid.com/api/api/` -> bare `404`, empty body, ASP.NET headers. So `/api` is a separate ASP.NET
  Web API app, not the SPA catch-all.
- **Login call**: `login(e,i){const a=this.encodeParams({grant_type:"password",username:e,password:i,`
  `clientId:this.clientId});return this.logout(),this.http.post("account/login",a,{headers:{"Content-Type":`
  `"application/x-www-form-urlencoded"}})`. Its caller is the login form, `this.authService.login(e.email,e.password)`,
  so username is the email address.
- Token handling, same class: `saveToken` does `localStorage.setItem("sgToken",JSON.stringify(o))`; the response is read
  for `o.refresh_token` and `e[".expires"]`. `access_token` / `refresh_token` / `.issued` / `.expires` is the OWIN
  `OAuthAuthorizationServerProvider` token shape. Refresh reuses the same endpoint:
  `{grant_type:"refresh_token",client_id:this.clientId,refresh_token:this.refreshToken}` -> `POST "account/login"`.
- `this.clientId` is never assigned anywhere in the bundle (verified by exhausting all `clientId` matches), so the
  browser really sends the literal `clientId=undefined`.
- **No CSRF/anti-forgery token anywhere**, and no cookie auth: the bearer token in `localStorage` is the only
  credential. (`consumption/source.py:_login` used to hint at scraping a hidden `__RequestVerificationToken`; that hint
  was wrong and has been removed.) **No OTP/SMS/2FA** either - the only `OTP` matches sit inside the string `FORGOTPASSWORD`, and the login UI
  strings are just `EMAIL`, `PASSWORD`, `SIGNIN`, `FORGOTPASSWORD`, `INVALIDUSER:"The user name or password is
  incorrect."`.
- **Consumption endpoints**, all relative to the base above:
  - `getConsumption(e,i,r,a,o,u,v){let y=`meterdata/consumption?meterId=${i}&period=${e}`;` then appended only when
    truthy: `&fromDate=`, `&toDate=`, `&includeComparative=`, `&compareFromDate=`, `&compareToDate=`. Dates are
    moment-formatted `MM/DD/YYYY`. Argument order: `(period, meterId, fromDate, toDate, includeComparative,
    compareFrom, compareTo)`.
  - `getMeterElectricitySummary(e){return this.http.get("meterdata/electricity/summary/"+e)}` and
    `getMeterWaterSummary(e){return this.http.get("meterdata/water/summary/"+e)}`
  - `sites/dashboard/consumption?siteId=${i}&period=${e}&meterType=${r}` + `&fromDate=` `&toDate=`;
    `meterdata/exportPDF?meterId=${i}&period=${e}`; `meterdata/compare?meterId=${e}&compareMeterId=${i}`;
    `POST meterdata/meterDataExport?&meterId=&fromDate=&toDate=` with `responseType:"blob"` -> `.xlsx`.
- **`period` is a string enum**: `"hourly"`, `"daily"`, `"monthly"`, `"yearly"` (from the `mat-select` options and the
  `switch(this.period)` blocks). Date window the UI picks per period: `hourly` -> `startOf("day")`..`endOf("day")`, one
  day per request; `daily` -> the month; `monthly` -> the year; `yearly` -> `` Wo(`${year}-01-01`).subtract(4,"year") ``,
  i.e. 5 calendar years in one call.
- Meter discovery: `getUserInfo` calls `this.http.get("user/info")`; the response carries `roles` (enum `User` /
  `SuperUser` / `Operator` / `Administrator`) and `addresses`, filtered by `i.addresses.filter(o=>!0===o.isActive)`.
  Each address holds `.meters`, and `loadAddressData(e)` reads `e.meters[n].meterId`. Chain: address -> meters -> meterId.
- Meter type enum: `Electricity=1, Water=2, Solar=3, Gaz=4, "WaterModbus-Bakard"=5, "ElectricityFTP-PLC"=6,`
  `ElectricityCOM=7`. Chart units: `this.units=this.IsWaterType?"m3":"KwH"` - matches `UNITS` in `consumption/source.py`.
- Languages: `[{id:"en",...,dir:"ltr"},{id:"he",...,dir:"rtl"}]`, defaulting to `languages[1]` (Hebrew, RTL); translations are embedded in `main.*.js`, so there is no server-side locale.
- `robots.txt` and `sitemap.xml` both return `200 text/html` with the identical 79579-byte SPA shell. Neither exists, and **a `200` on `www.mycitygrid.com` proves nothing about a path**. No `swagger`, `openapi` or `/api/docs` string appears anywhere in the bundle.
- Operator: the bundle links `https://apps.apple.com/ua/app/my-city-grid/id1520663116` and
  `https://play.google.com/store/apps/details?id=com.mycitygrid` (both 404 for us now), and
  `http://quickode.com/portfolio/Smart%20Grid` states: "Smart Grid, crated by Quickode for Einat-Asik Infrastructures
  Ltd. allows you to monitor, manage and track Electric, Gas, Water and gas meters of several brands." Nav items
  (`Sites`, `Readers`, `Tariffs`, `Noga-Managment`) point to a multi-tenant utility platform, not one municipality.

## Best guess at the login flow

Hypothesis, untested. `POST https://www.mycitygrid.com/api/api/account/login`, header
`Content-Type: application/x-www-form-urlencoded`, body `grant_type=password&username=<email>&password=<pass>&`
`clientId=undefined` with each value percent-encoded (the app's `encodeParams` runs `encodeURIComponent` per value;
`clientId=undefined` mimics the browser, and dropping the field is the first thing to try if it fails). Expect `200` with
`{"access_token":...,"token_type":"bearer","expires_in":...,"refresh_token":...,".issued":...,".expires":...}`, and
`400 {"error":"invalid_grant"}` on bad credentials. Then send `Authorization: Bearer <access_token>` on every later
request. Cookies are irrelevant here, so `_login` must stash the token on the session
(`session.headers["Authorization"] = ...`) rather than lean on `FetcherSession` cookie persistence; refresh by
re-posting the same URL with `grant_type=refresh_token&client_id=undefined&refresh_token=<rt>` before `.expires`.

## Best guess at the consumption endpoints

Hypothesis, untested. All relative to `https://www.mycitygrid.com/api/api/`.

1. `GET user/info` -> take the active address, then its `meters[]`; keep `meterId` where `type == 1` for electricity and
   `type == 2` for water.
2. `GET meterdata/consumption?meterId=<id>&period=hourly&fromDate=MM/DD/YYYY&toDate=MM/DD/YYYY`, looping one local day
   per request as the UI does. Omit `includeComparative`, `compareFromDate` and `compareToDate` - the UI omits them when
   falsy.
3. Response shape, inferred from `subscribe(i=>{this.chartDateValue=i.name,this.chartData=i.values` and
   `this.chartData[0].series.map(o=>o.name)`: the ngx-charts grouped-bar format
   `{"name":"<label>","values":[{"name":"<bucket>","series":[{"name":"<series>","value":<number>}]}]}`. Series count is
   meaningful - the code branches on `6===r.length` (non-domestic, time-of-use bands) versus fewer (domestic). Values
   look like per-bucket consumption, not cumulative, since a multiplier is applied per point
   (`i.value=i.value/this.waterMultiplier*.1`) - confirm before writing `_fetch_range`.
4. Backfill alternative: `POST meterdata/meterDataExport?&meterId=<id>&fromDate=&toDate=` returns an `.xlsx` over an
   arbitrary range, possibly years of raw rows in one request. Whether a `User`-role account may call it is unknown.

## Unknowns that only credentials can answer

`test-connection.bat` now answers most of this without a browser: it logs in once and writes `user/info`, its meters and
their types, and one day of hourly buckets per meter to `data/connection-report.txt`, redacted, plus whether
`consumption/readings.py` understood each response and whether the values look cumulative rather than per-hour. What it
cannot answer is the wider-window question and how far back history goes; the report lists those as open. Otherwise,
sign in at `https://www.mycitygrid.com/login` with the network tab recording, then capture:

- [ ] The exact `account/login` body and response JSON - is `clientId` required, what is `expires_in`, and what error
      shape comes back on failure.
- [ ] `user/info` in full: role, `addresses[].addressId`, `meters[].meterId`, `meters[].type`.
- [ ] One `meterdata/consumption?...&period=hourly` request and response verbatim: the bucket `name` format (`"00:00"`,
      `"0"`, an ISO timestamp?), the `series` names, the timezone, and whether a DST-change day returns 23 or 25 buckets.
- [ ] Whether values are per-hour deltas or cumulative readings, and what `waterMultiplier` and `isSenssus` are for this
      household's water meter.
- [ ] How far back `fromDate` may go before responses come back empty, whether `meterdata/meterDataExport` is permitted for a household account, and any request header beyond `Authorization` that the API insists on.

## Dead ends

- `robots.txt` and `sitemap.xml` both return the SPA shell; no machine-readable site map exists. `GET /api/api/` gives a
  bare `404` with no index or discovery document, and the bundle has no `swagger` / `openapi` / `/api/docs` reference.
- Web search found no documentation and no existing integration. Terms tried: "mycitygrid.com Quickode water electricity
  meter reading Israel municipality"; "mycitygrid API reverse engineer Home Assistant integration"; "My City Grid app
  Einat Asik meters consumption hourly". The nearest neighbour is `github.com/tsvi/city4u_water_meter`, a Home Assistant
  component for the unrelated City4U platform - useful only as a shape to copy.
- Both mobile store listings linked from the bundle now 404, so no marketing copy about granularity or history depth is publicly available. The `hourly` chart option and the 5-year `yearly` window are the only granularity evidence, and both come from code, not from any published claim.
