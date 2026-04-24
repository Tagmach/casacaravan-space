// ── Casa Caravan Space — Page Tracking ───────────────────────────
(function(){
  const SUPA_URL='https://iwfvlatywksvnnxymweb.supabase.co';
  const SUPA_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3ZnZsYXR5d2tzdm5ueHltd2ViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5ODE0NDEsImV4cCI6MjA5MjU1NzQ0MX0.nHjA1dQHZG6ey9XwpvbN3mjQmAv4DZ4CB1CkC7hWens';

  const page = location.pathname.replace('/', '') || 'index';
  const referrer = document.referrer ? new URL(document.referrer).hostname : 'direct';
  const startTime = Date.now();

  // Send visit on page unload with duration
  function sendVisit(duration){
    const body = JSON.stringify({
      page, referrer,
      duration_seconds: Math.round(duration / 1000)
    });
    navigator.sendBeacon(
      SUPA_URL + '/rest/v1/page_visits',
      new Blob([body], {type:'application/json'})
    );
  }

  // Also try fetch with keepalive as fallback
  function sendVisitFetch(duration){
    fetch(SUPA_URL + '/rest/v1/page_visits', {
      method: 'POST',
      keepalive: true,
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPA_KEY,
        'Authorization': 'Bearer ' + SUPA_KEY,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify({
        page, referrer,
        duration_seconds: Math.round(duration / 1000)
      })
    }).catch(()=>{});
  }

  window.addEventListener('pagehide', ()=>{
    const duration = Date.now() - startTime;
    sendVisitFetch(duration);
  });

  window.addEventListener('beforeunload', ()=>{
    const duration = Date.now() - startTime;
    sendVisitFetch(duration);
  });
})();
