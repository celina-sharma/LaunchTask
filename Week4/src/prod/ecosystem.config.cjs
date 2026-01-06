module.exports = {
  apps: [
    {
      name: "week4-api",
      cwd: "/home/celinasharma/Desktop/LaunchPad1/Week4/src",
      script: "index.js",
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      env: {
        NODE_ENV: "development",
        PORT: 5000
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 5000
      }
    },
    {
      name: "email-worker",
      cwd: "/home/celinasharma/Desktop/LaunchPad1/Week4/src",
      script: "workers/email.worker.js",
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false
    }
  ]
};