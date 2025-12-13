#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);

const flag = args[0];
const files = args.slice(1);

if (!flag || files.length === 0) {
  console.log("Usage: node stats.js (-lines|--words|--chars|--unique) file1 file2 ...");
  process.exit(1);
}

function countLines(text) {
  return text.split("\n").length;
}

function countWords(text) {
  return text.trim().split(/\s+/).length;
}

function countChars(text) {
  return text.length;
}

function removeDuplicates(text) {
  const lines = text.split("\n");
  const uniqueLines = [...new Set(lines)];
  return uniqueLines.join("\n");
}

files.forEach((file) => {
  const content = fs.readFileSync(file, "utf8");

  if (flag === "--lines") {
    console.log(`${file}: ${countLines(content)} lines`);
  } else if (flag === "--words") {
    console.log(`${file}: ${countWords(content)} words`);
  } else if (flag === "--chars") {
    console.log(`${file}: ${countChars(content)} characters`);
  } else if (flag === "--unique") {
    const uniqueContent = removeDuplicates(content);

    const outputDir = path.join(__dirname, "output");
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir);
    }

    const outputFile = path.join(outputDir, "unique-" + path.basename(file));  //This line creates the full path to the new file.
    fs.writeFileSync(outputFile, uniqueContent, "utf8");

    console.log(`${file}: Unique lines saved to ${outputFile}`);
  } else {
    console.log("Unknown flag");
  }
});
