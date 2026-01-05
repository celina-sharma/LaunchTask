Manual Security test cases :->
 
1. Payload whitelisting:->
    {
  "name": "Phone",
  "price": 300,
  "isAdmin": true -> Extra field isAdmin shouldn't be accepeted
}
 
Result :->
  {
  "success": false,
  "message": "Invalid input: unrecognized key(s)",
  "code": 400
  }
 
 
2.Wrong Datatype :->  
    API: POST/products
    {
      "name": "Phone",
      "price": "cheap" -> String provided where number is required(Schema validation failure)
    }
 
 
Result :->
    {
    "success": false,
    "message": "Validation error",
    "errors": [
        "Invalid input: expected number, received string"
    ]
}
 
3.NoSQL injection :->
 API: POST/products
    {
     "name": { "$gt": "" }, -> object injected instead of string(validation rejects payload)
     "price": 500
    }  
 
 
Result :->
    {
    "success": false,
    "message": "Validation error",
    "errors": [
        "Invalid input: expected string, received object"
    ]
} 
 
4. Rate limiting :->
 
max = 10 , times a user can hit this end point :-> 1 minute
API: GET/products
 
Hitting more than that : ->
 
res =>  Too many requests, please try again later.
{
  "success": false,
  "message": "Too many requests, please try again later",
  "code": 429
}
 
5. Paload Size limits :->
 
max size of the payload  :-> 10kb
 
 
GET/http://localhost:3000/products/
 
and json body :->
 
{
    "name" : "celina sharma",
    "desscription" : "Too large", // this make this json payload size more than 10 kb
    "price" : 80000
}
 
Res => PayloadTooLargeError: request entity too large
    {
    "success": false,
    "message": "request entity too large",
    "code": 413,
    "timestamp": "2026-01-05T12:13:54.092Z",
    "path": "/products"
    }
 
6. helmet() => Nodejs middleware for experss
  eg -> Different origin cannot embed our site page : in an iframe :
 
  API: GET/products
  Expected Headers:

  X-Content-Type-Options
  X-Frame-Options
  Referrer-Policy
  X-DNS-Prefetch-Control


8.  Centralized Error Handling Validation

   API: Send any invalid request

   Expected Response format:

  {
    "success": false,
    "message": "Error message",
    "code": 400,
    "timestamp": "...",
    "path": "/products"
  }
