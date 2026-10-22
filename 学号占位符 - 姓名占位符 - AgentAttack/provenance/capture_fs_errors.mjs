// Diagnostics only: preserve operation semantics and log underlying filesystem errors.
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
const append=fs.appendFileSync.bind(fs);
const log=(op,e)=>{
 if(!process.env.COURSE_DIAGNOSTIC_PATH||['ENOENT','EEXIST','ENOTEMPTY'].includes(e?.code))return;
 try{append(process.env.COURSE_DIAGNOSTIC_PATH,JSON.stringify({timestamp:new Date().toISOString(),operation:op,code:e?.code,message:e?.message,stack:e?.stack})+'\n')}catch{}
};
for(const op of ['mkdirSync','openSync','chmodSync','writeFileSync','renameSync','lstatSync']){
 const original=fs[op];fs[op]=function(...args){try{return original.apply(this,args)}catch(e){log(op,e);throw e;}};
}
syncBuiltinESMExports();
// OpenClaw's GatewayLockError assigns cause after super(); retain that original cause.
Object.defineProperty(Error.prototype,'cause',{
 configurable:true,
 set(value){
  Object.defineProperty(this,'cause',{value,writable:true,configurable:true,enumerable:true});
  if(String(this.message).includes('failed to acquire gateway state ownership')){
   try{append(process.env.COURSE_DIAGNOSTIC_PATH,JSON.stringify({timestamp:new Date().toISOString(),operation:'GatewayLockError.cause',cause_name:value?.name,code:value?.code,message:value?.message,stack:value?.stack})+'\n')}catch{}
  }
 }
});
