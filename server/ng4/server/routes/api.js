const express = require('express');
const router = express.Router();
var fs = require('file-system');
var MongoClient = require('mongodb').MongoClient , assert = require('assert');
var randomstring = require("randomstring");
var natural = require('natural');
const http = require('http');

// Connection URL
var url = 'mongodb://localhost:27017/articles';

var mongodb;






MongoClient.connect(url, {
        poolSize: 10
        // other options can go here
    },function(err, db) {
        //assert.equal(null, err); to fix it later
        mongodb=db;
	

    }
)


var pagesize = 5;
var subjectivity = 0.3;

var polarity = {"negative" : -0.05, "positive":0.1, "neutralb1": -0.05, "neutralb2":0.1};


















natural.PorterStemmer.attach();




router.get('/query', (req, res, next) => {






tokens = req.query.query.toLowerCase().tokenizeAndStem();
finalQuery = tokens.join('|');
author = typeof req.query.author =='undefined'?".*":req.query.author.toLowerCase().tokenizeAndStem().join('|');
dateSort = typeof req.query.dateSort =='undefined'?"desc": req.query.dateSort;
category = typeof req.query.category =='Any'?".*": req.query.category;





query = {"sentences":{$elemMatch:{"sentence":{ '$regex' : finalQuery, '$options' : 'i' }, "subjectivity":{$gt:subjectivity}, 

$and:[ req.query.polarity=="negative" ? {"polarity":{$lt:polarity["negative"]}} : req.query.polarity=="positive"? {"polarity":{$gt:polarity["positive"]}}: {"polarity":{$gt:polarity["neutralb1"]}, "polarity":{$lt:polarity["neutralb2"]}}    ]}}};
	


findArticle = mongodb.collection("articles").find(query,{"body":0},{"sort" : [['date', dateSort]]} );




findArticle.count(function (e, count) {

// Use count here

    
findArticle.skip(pagesize*(req.query.page-1)).limit(pagesize).toArray(function (err, result1) {
    if (err) throw err;


    for(i=0;i<result1.length;i++)
{
		 for(j=0;j<result1[i]["sentences"].length;j++)
	{
			 for(k=0;k<tokens.length;k++)
		{
			if(result1[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k])!=-1 && (req.query.polarity=="negative"? result1[i]["sentences"][j]["polarity"]<polarity["negative"]:req.query.polarity=="positive" ?result1[i]["sentences"][j]["polarity"]>polarity["positive"]:(result1[i]["sentences"][j]["polarity"]>polarity["neutralb1"] && result1[i]["sentences"][j]["polarity"]< polarity["neutralb2"])))
		{
			if(result1[i]["sentences"][j]["keys"]==null)
		{
			result1[i]["sentences"][j]["keys"] = [];
			result1[i]["sentences"][j]["keys"].push(result1[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k]));
		}else
		{
			result1[i]["sentences"][j]["keys"].push(result1[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k]));
		}
	
	
		}
	

		}

	}
}


    finalRes = {"data":result1, "suggestion":["dummy1","dummy2","dummy3"],"meta":{"count":count, "page": parseInt(req.query.page), "pages": Math.ceil(count/pagesize)}};


    res.json(finalRes);
   
    
});



});











});













router.post('/validate', (req, res, next) => {




try {
	mongodb.collection("evaluation").insertOne( req.body );	
	res.send(200); 
	
} catch (err) {
 
	res.send(400);

}









});









































router.get('/procontra', (req, res, next) => {






tokens = req.query.query.toLowerCase().tokenizeAndStem();
finalQuery = tokens.join('|');
author = typeof req.query.author =='undefined'?".*":req.query.author.toLowerCase().tokenizeAndStem().join('|');
dateSort = typeof req.query.dateSort =='undefined'?"desc": req.query.dateSort;
category = typeof req.query.category =='Any'?".*": req.query.category;






console.log(tokens);




query1 = {"sentences":{$elemMatch:{"sentence":{ '$regex' : finalQuery, '$options' : 'i' }, "subjectivity":{$gt:subjectivity},"polarity":{$lt:polarity["negative"]} }}};
query2 = {"sentences":{$elemMatch:{"sentence":{ '$regex' : finalQuery, '$options' : 'i' }, "subjectivity":{$gt:subjectivity},"polarity":{$gt:polarity["positive"]} }}};
	
	


findNegativeArticle = mongodb.collection("articles").find(query1,{"body":0},{"sort" : [['date', dateSort]]} );
findPositiveArticle = mongodb.collection("articles").find(query2,{"body":0},{"sort" : [['date', dateSort]]} );




findNegativeArticle.count(function (e, count) {

// Use count here

negativeCount = count;
    
findNegativeArticle.skip(pagesize*(req.query.page-1)).limit(pagesize).toArray(function (err, result1) {
    if (err) throw err;


    for(i=0;i<result1.length;i++)
{
	 for(j=0;j<result1[i]["sentences"].length;j++)
{
	 for(k=0;k<tokens.length;k++)
{

	if(result1[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k])!=-1  && result1[i]["sentences"][j]["polarity"]<polarity["negative"])
{
	if(result1[i]["sentences"][j]["keys"]==null)
{
result1[i]["sentences"][j]["keys"] = [];
result1[i]["sentences"][j]["keys"].push(result1[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k]));
}else
{
result1[i]["sentences"][j]["keys"].push(result1[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k]));
}
	
	
}
	

}

}
}





findPositiveArticle.count(function (e, count) {

// Use count here

positiveCount = count;
    
findPositiveArticle.skip(pagesize*(req.query.page-1)).limit(pagesize).toArray(function (err, result) {
    if (err) throw err;


    for(i=0;i<result.length;i++)
{
	 for(j=0;j<result[i]["sentences"].length;j++)
{
	 for(k=0;k<tokens.length;k++)
{

	if(result[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k])!=-1  && result[i]["sentences"][j]["polarity"]>polarity["positive"])
{
	if(result[i]["sentences"][j]["keys"]==null)
{
result[i]["sentences"][j]["keys"] = [];
result[i]["sentences"][j]["keys"].push(result[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k]));
}else
{
result[i]["sentences"][j]["keys"].push(result[i]["sentences"][j]["sentence"].toLowerCase().indexOf(tokens[k]));
}
	
	
}
	

}

}
}


proContraElem = [];

finalCount = Math.min(positiveCount,negativeCount)

    for(i=0;i<result.length;i++)
{

    proContraElem.push({"pro":result[i], "contra":result1[i]});
}

    finalRes = {"data":proContraElem,"suggestion":["dummy1","dummy2","dummy3"], "meta":{"count":finalCount, "page": parseInt(req.query.page), "pages": Math.ceil(finalCount/pagesize)}};


    res.json(finalRes);
   
    
});



});






 
    
});



});











});










router.get('/autocomplete', (req, res, next) => {




    



http.get('http://127.0.0.1:5000/generateautocomplete?query='+req.query.query, (resp) => {
  let data = '';
 
  // A chunk of data has been recieved.
  resp.on('data', (chunk) => {
    data += chunk;
    res.send(data);
  });
 

 
}).on("error", (err) => {

  console.log("Error: " + err.message);

});







});






// Error handling
const sendError = (err, res) => {
    response.status = 501;
    response.message = typeof err == 'object' ? err.message : err;
    res.status(501).json(response);
};

// Response handling
let response = {
    status: 200,
    data: [],
    message: null
};



module.exports = router;
