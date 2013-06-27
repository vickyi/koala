Nearby Search Requests

Earlier versions of the Places API referred to Nearby Search as Place Search.

A Nearby Search lets you search for Places within a specified area. You can refine your search request by supplying keywords or specifying the type of Place you are searching for.

A Nearby Search request is an HTTP URL of the following form:

https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters
where output may be either of the following values:

json (recommended) indicates output in JavaScript Object Notation (JSON)
xml indicates output as XML
Certain parameters are required to initiate a Nearby Search request. As is standard in URLs, all parameters are separated using the ampersand (&) character.

Required parameters

key — Your application's API key. This key identifies your application for purposes of quota management and so that Places added from your application are made immediately available to your app. Visit the APIs Console to create an API Project and obtain your key.
location — The latitude/longitude around which to retrieve Place information. This must be specified as latitude,longitude.
radius — Defines the distance (in meters) within which to return Place results. The maximum allowed radius is 50 000 meters. Note that radius must not be included if rankby=distance (described under Optional parameters below) is specified.
sensor — Indicates whether or not the Place request came from a device using a location sensor (e.g. a GPS) to determine the location sent in this request. This value must be either true or false.
Optional parameters

keyword — A term to be matched against all content that Google has indexed for this Place, including but not limited to name, type, and address, as well as customer reviews and other third-party content.
language — The language code, indicating in which language the results should be returned, if possible. See the list of supported languages and their codes. Note that we often update supported languages so this list may not be exhaustive.
minprice and maxprice (optional) — Restricts results to only those places within the specified range. Valid values range between 0 (most affordable) to 4 (most expensive), inclusive. The exact amount indicated by a specific value will vary from region to region.
name — A term to be matched against the names of Places. Results will be restricted to those containing the passed name value. Note that a Place may have additional names associated with it, beyond its listed name. The API will try to match the passed name value against all of these names; as a result, Places may be returned in the results whose listed names do not match the search term, but whose associated names do.
opennow — Returns only those Places that are open for business at the time the query is sent. Places that do not specify opening hours in the Google Places database will not be returned if you include this parameter in your query.
rankby — Specifies the order in which results are listed. Possible values are:
prominence (default). This option sorts results based on their importance. Ranking will favor prominent places within the specified area. Prominence can be affected by a Place's ranking in Google's index, the number of check-ins from your application, global popularity, and other factors.
distance. This option sorts results in ascending order by their distance from the specified location. Ranking results by distance will set a fixed search radius of 50km. One or more of keyword, name, or types is required.
types — Restricts the results to Places matching at least one of the specified types. Types should be separated with a pipe symbol (type1|type2|etc). See the list of supported types.
pagetoken — Returns the next 20 results from a previously run search. Setting a pagetoken parameter will execute a search with the same parameters used previously — all parameters other than pagetoken will be ignored.
zagatselected — Restrict your search to only those locations that are Zagat selected businesses. This parameter does not require a true or false value, simply including the parameter in the request is sufficient to restrict your search. The zagatselected parameter is experimental, and only available to Places API enterprise customers.
Maps API for Business customers should not include a client or signature parameter with their requests.

An example request is below, showing a search for Places of type 'food' within a 500m radius of a point in Sydney, Australia, containing the word 'harbour' in their name:

https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&types=food&name=harbour&sensor=false&key=AddYourOwnKeyHere

Note that you'll need to replace the key in this example with your own key in order for the request to work in your application.