const { contextBridge } = require("electron");
contextBridge.exposeInMainWorld("plotlight", {});
