# Implementation Notes
The core assignment was to design and implement a new API to connect with the 3P House Canary API to return information on whether a given address has a septic system.

The frontend will then use this information to determine whether to prompt for additional questions. It is possible to abstract this API to focus on whether the frontend should prompt for an additional question instead of whether the house has a septic system. But ultimately determining business logic like this is probably best left for the frontend as there could be scenarios in the future that need access to whether they have a septic system and there could be different flows using this API that need different logic (ex: condo vs. single family home). In a workplace setting, this would be an important conversation to have with the product manager and the frontend engineers to validate that this assumption is correct.

## Installation Guide
```bash
[git clone this repo]
cd [cloned directory]
pipenv shell
pipenv install flask

[Update environment variables in .env]
flask run
```

To run the tests, within the pipenv shell run
```bash
pytest
```

## API Design
2XX
* 200 - isSeptic yes/no
* 204 - No content. Address / Sewer information could not be found in the DB
4XX - Unable to return results
* 400 Missing required param
* 401 Auth failed
* 429 Too many requests

## Flask
I decided to use Flask for this assignment because it has a lightweight setup process, good documentation, and creating APIs is pretty straightforward.

# Cost
If we found out we were spending too much on Home Canary and needed to reduce costs, we could consider:
- Restructuring the frontend to make less calls to this API (if possible)
- Introducing a caching layer. Sewer data for a building is unlikely to change frequently so there could be a very high TTL (6 months?). However, most users will only use these flows from HomeTap once so the caching may not be worth the storage costs.
- Home Canary has an alternative Match and Append app which could be a one-time cost to get the data and then this data could be refreshed every 6-12 months if needed.
- Home Canary notes that they do not charge for 204 errors (if the address is not found in their DB) so optimizing for verifying the address would not help.
- Adjusting testing workflows to ensure we're not calling the API too many times ourselves. We would especially want to understand the rate limiting and ensure that integration testing is not at risk of hitting the threshold and preventing actual customers from using the APIs.

However, all of these would be likely be over-optimizations depending on the problem space and should only be investigated if cost reduction is a primary concern.

# Security/Scalability/Maintainability

Many of these ideas would be overkill for V1, but would be good to generally discuss
in the initial design meeting and determine as a team the priority/timeline for addressing (if at all).

* Ensure the engineering team is aware of the rate limit that you agreed to with the accounts team so this can be considered when developing tests and building out new features. There should be alarms when approaching 70% and 90% of the limit. If a new feature might cause the limit to be reached, this should be flagged as soon as possible so there can be a technical workaround, a functionality workaround, or a new agreement with Home Canary for a higher rate.
* We are paying for the property/details call, but we are only using one element of the call. If we anticipate gaining additional value from this API, it would be best to cache the entire response. Clients could use GraphQL or a similar approach to only ask for what they need or the API created during this assignment could use GraphQL to do this.
* Authentication was not implemented as part of this, but this API should live in the backend and use the same authentication solutions used elsewhere for the app. Any caching solution selected should ensure data is encrypted.
* API keys should remain secure in the backend and not accessible on the client. They should not be checked into the code, but stored securely via a secrets manager or other secure process.
* If it is possible, configure that the API keys can only be used on relevant HomeTap domains via Home Canary. This will prevent the API keys from being usable even if they are compromised.
* In case of a suspected breach or on a regular cadence, rotate the keys.

# Next steps
* The documentation indicates that the 3P api can accept **address** (where the apartment unit is included in **address**) or can accept **address** and **unit**. Although beyond the scope of this assignment, to make this API more robust in the future it would probably be best to collect address and unit separately from the frontend, assuming the frontend already has access to this information. If we integrate with additional APIs in the future or if House Canary starts requiring unit separately, this will ensure we have the right information.
* For now the API we created requires that the address is formatted correctly/is a valid address. There is not additional validation done. Since HouseCanary does not charge for API calls when the address is not valid, there isn't a cost associated with this, but it will result in a delay on the client for an issue that is larger than whether they have a septic tank.

# Topics to discuss with the team

## Engineering
- How will the frontend use this API? What are their requirements?
- Is it more useful to have a generic septic api or is it more useful to have a API for when to prompt to ask additional questions?
- Based on the existing logic, will the client have already verified that this is a valid address (ex: with previous api calls for prior steps) or do we want to implement verification server side?

## Product
- In the event that we cannot determine septic status (API outage, rate limit hit, address not found, etc.), what will we do on the frontend?
- How important is speed vs. accuracy vs. cost when it comes to caching this information?
- How much do we want to invest in future proofing this API now vs. launching V1 more quickly? What is the likelihood that we want to change the source of where we're getting the septic information in the next 6 months, 12 months?
- What does our contract look like with Home Canary? What is our current rate limit? Are there requirements or rules about caching the data?
