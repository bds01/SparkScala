var person = {key1:{ fname: "Nick", lname: "Jonas", age: 26 }, key2:{ fname: "James", lname: "Phillips", age: 46 }};

for (var key in person) {
    // skip loop if the property is from prototype
    if (!person.hasOwnProperty(key)) continue;

    var obj = person[key];
    for (var prop in obj) {
        // skip loop if the property is from prototype
        if (!obj.hasOwnProperty(prop)) continue;

        // your code
        console.log(prop + " = " + obj[prop]);
    }
}
