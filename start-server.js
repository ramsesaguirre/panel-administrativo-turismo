const { exec } = require('child_process');

exec('npx serve', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  console.log(stdout);
  console.log('Server started - manually copy this URL to your browser:');
  console.log('http://localhost:3000');
});
