// ── Casa Caravan Space — Page Tracking ───────────────────────────
(function(){
  const SUPA_URL='https://iwfvlatywksvnnxymweb.supabase.co';
  const SUPA_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3ZnZsYXR5d2tzdm5ueHltd2ViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5ODE0NDEsImV4cCI6MjA5MjU1NzQ0MX0.nHjA1dQHZG6ey9XwpvbN3mjQmAv4DZ4CB1CkC7hWens';

  const allowed=['casacaravan.space','localhost','127.0.0.1','claudeusercontent.com'];
  if(!allowed.some(a=>location.hostname.includes(a))) return;

  const page=location.pathname.split('/').pop()||'index.html';
  const ref=document.referrer;
  const referrer=ref?(()=>{try{return new URL(ref).hostname;}catch(e){return'direct';}})():'direct';
  const startTime=Date.now();

  function post(dur){
    fetch(SUPA_URL+'/rest/v1/page_visits',{
      method:'POST',
      keepalive:true,
      headers:{
        'Content-Type':'application/json',
        'apikey':SUPA_KEY,
        'Authorization':'Bearer '+SUPA_KEY,
        'Prefer':'return=minimal'
      },
      body:JSON.stringify({page,referrer,duration_seconds:dur})
    }).catch(()=>{});
  }

  // Record on load
  post(0);

  // Update on leave
  function onLeave(){
    const dur=Math.round((Date.now()-startTime)/1000);
    if(dur>2) post(dur);
  }
  window.addEventListener('pagehide',onLeave);
  window.addEventListener('beforeunload',onLeave);
  document.addEventListener('visibilitychange',()=>{
    if(document.visibilityState==='hidden') onLeave();
  });
})();
