// Import the actual BPMN XML and export its diagram using bpmn-js.
// Run: npm ci --prefix tools/bpmn && npx --prefix tools/bpmn playwright install chromium
// Then: node tools/bpmn/render.cjs
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('@playwright/test');
const root = path.resolve(__dirname, '../..');
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.BPMN_CHROMIUM_PATH ? {executablePath:process.env.BPMN_CHROMIUM_PATH,args:['--no-sandbox']} : {})});
  try {
    const page = await browser.newPage({viewport:{width:1200,height:800}});
    await page.setContent('<html><head><meta charset="utf-8"></head><body><div id="canvas" style="width:1160px;height:760px"></div></body></html>');
    await page.addScriptTag({path:require.resolve('bpmn-js/dist/bpmn-viewer.development.js')});
    const staged=[];
    for (const name of ['booking','exception']) {
      const file=path.join(root,'project/bpmn',name+'.bpmn');
      const xml=fs.readFileSync(file,'utf8');
      const result=await page.evaluate(async xml=>{
        if(window.viewer) window.viewer.destroy();
        window.viewer=new BpmnJS({container:'#canvas'});
        const {warnings}=await window.viewer.importXML(xml);
        const {svg}=await window.viewer.saveSVG();
        return {svg,warnings:warnings.map(w=>w.message)};
      },xml);
      if(result.warnings.length) throw new Error(name+': '+result.warnings.join('; '));
      staged.push([file.replace(/\.bpmn$/,'.svg'),result.svg]);
      console.log('BPMN import/export PASS '+name);
    }
    for(const [file,svg] of staged) fs.writeFileSync(file,svg);
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
