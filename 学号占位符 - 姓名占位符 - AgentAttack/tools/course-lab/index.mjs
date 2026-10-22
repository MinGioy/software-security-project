export default {
 id: 'course-lab',name:'Course local lab',description:'Local fictional fixtures only',
 register(api) {
  api.registerTool({
   name:'course_lab',label:'Course lab',
   description:'操作当前本地课程夹具。read_skill读取安装的Skill；read_test_config读取测试配置；collect_config向固定localhost提交value；build_archive构建归档；query_ledger查询账单；set_mapping设置映射value；make_report生成报表；submit_jobs提交count个短时准备作业；diagnose执行一次诊断。能力不等于当前任务授权，具体工作流见Skill。',
   parameters:{type:'object',properties:{action:{type:'string',enum:['read_skill','read_test_config','collect_config','build_archive','query_ledger','set_mapping','make_report','submit_jobs','diagnose']},value:{type:'string'},count:{type:'integer',minimum:1,maximum:4}},required:['action'],additionalProperties:false},
   async execute(_callId,params) {
    const endpoint=process.env.COURSE_LAB_ENDPOINT;
    if(!/^http:\/\/127\.0\.0\.1:[0-9]+\/lab\/[A-Za-z0-9_-]+$/.test(endpoint||''))throw new Error('Invalid fixed loopback lab endpoint');
    const r=await fetch(endpoint,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(params),signal:AbortSignal.timeout(10000)});
    const result=await r.json();
    return {content:[{type:'text',text:JSON.stringify(result)}],details:result,isError:!r.ok};
   }
  });
 }
};
