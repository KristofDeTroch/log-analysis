import fs from 'fs';
import path from 'path';

const inputPath = './cf-2023-06-28-raw'; // Replace this with the path to your CSV files folder
const outputPath = './cf-2023-06-28-processed';
function restructureFirstLine(fileName: string) {

    const inputFilePath = path.join(inputPath, fileName);
  const content = fs.readFileSync(inputFilePath, 'utf-8');
  const lines = content.trim().split('\n').slice(1);
  
  if (lines.length > 0) {
    const firstLine = lines[0];
    const headers = firstLine.split(' ');

    // Remove the leading '#' character from each header and join them with a tab separator
    const modifiedFirstLine = headers.slice(1).join('\t');

    // Replace the first line in the content with the modified version
    lines[0] = modifiedFirstLine;

    const updatedContent = lines.join('\n');
    const outputFilePath = path.join(outputPath, fileName);
    fs.writeFileSync(outputFilePath, updatedContent, 'utf-8');
  }
}

function restructureAllCSVFiles(folderPath: string) {
  fs.readdirSync(folderPath).forEach((file) => {
    if (path.extname(file) === '.csv') {
      restructureFirstLine(file);
    }
  });
}

restructureAllCSVFiles(inputPath);