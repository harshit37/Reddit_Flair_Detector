const express = require("express");
const path = require("path");
const app = express();
const fs = require('fs');
//joining path of directory
const directoryPath = path.join(__dirname, 'dist/flair-detection');
//passsing directoryPath and callback function
fs.readdir(directoryPath, function (err, files) {
    //handling error
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }
    //listing all files using forEach
    files.forEach(function (file) {
        // Do whatever you want to do with the file
        console.log(file);
    });
});

app.use(express.static(__dirname + '/dist/flair-detection'));
app.listen(process.env.PORT || 3000);
app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname, 'dist/flair-detection/index.html'));
})

console.log(__dirname);
console.log(process.env.PORT);
console.log(path.join(__dirname, 'dist/flair-detection/index.html'));
console.log('Console listening');