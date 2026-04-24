// ── Casa Caravan Space — Key System ──────────────────────────────
const CC_KEYS = (function(){
  const SUPA_URL='https://iwfvlatywksvnnxymweb.supabase.co';
  const SUPA_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3ZnZsYXR5d2tzdm5ueHltd2ViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5ODE0NDEsImV4cCI6MjA5MjU1NzQ0MX0.nHjA1dQHZG6ey9XwpvbN3mjQmAv4DZ4CB1CkC7hWens';

  let player = JSON.parse(localStorage.getItem('cc_player')||'null');
  let showing = false;

  // CSS — inject once
  const style = document.createElement('style');
  style.textContent = `
    #cc-key-overlay{
      position:fixed;inset:0;z-index:1000;
      display:flex;align-items:center;justify-content:center;
      background:rgba(6,5,10,0.92);
      opacity:0;pointer-events:none;transition:opacity 0.5s;
    }
    #cc-key-overlay.show{opacity:1;pointer-events:all;}
    #cc-key-box{
      text-align:center;
      transform:translateY(20px);transition:transform 0.5s;
    }
    #cc-key-overlay.show #cc-key-box{transform:translateY(0);}
    #cc-key-svg{
      width:120px;height:120px;margin:0 auto 24px;
      filter:drop-shadow(0 0 20px rgba(200,168,74,0.6));
      animation:keyGlow 2s ease-in-out infinite;
    }
    @keyframes keyGlow{
      0%,100%{filter:drop-shadow(0 0 16px rgba(200,168,74,0.5));}
      50%{filter:drop-shadow(0 0 32px rgba(200,168,74,0.9));}
    }
    #cc-key-num{
      font-family:'Cormorant Garamond',serif;
      font-size:11px;letter-spacing:4px;color:#c8a84a;
      text-transform:uppercase;margin-bottom:10px;
    }
    #cc-key-name{
      font-family:'Cormorant Garamond',serif;
      font-size:28px;font-weight:300;color:#D2C3AF;
      margin-bottom:8px;
    }
    #cc-key-msg{
      font-family:'Cormorant Garamond',serif;
      font-size:15px;font-style:italic;color:#7A7068;
      margin-bottom:32px;max-width:300px;margin-left:auto;margin-right:auto;
      line-height:1.7;
    }
    #cc-key-btn{
      font-family:'Jost',sans-serif;font-size:9px;letter-spacing:2.5px;
      text-transform:uppercase;padding:11px 28px;
      background:none;border:1px solid #c8a84a;color:#c8a84a;
      border-radius:100px;cursor:pointer;transition:all 0.2s;
    }
    #cc-key-btn:hover{background:rgba(200,168,74,0.1);}
  `;
  document.head.appendChild(style);

  // Overlay HTML
  const overlay = document.createElement('div');
  overlay.id='cc-key-overlay';
  overlay.innerHTML=`
    <div id="cc-key-box">
      <svg id="cc-key-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="35" cy="40" r="18" stroke="#c8a84a" stroke-width="3"/>
        <circle cx="35" cy="40" r="10" stroke="#c8a84a" stroke-width="1.5" opacity="0.4"/>
        <line x1="53" y1="40" x2="82" y2="40" stroke="#c8a84a" stroke-width="3" stroke-linecap="round"/>
        <line x1="75" y1="40" x2="75" y2="52" stroke="#c8a84a" stroke-width="3" stroke-linecap="round"/>
        <line x1="82" y1="40" x2="82" y2="48" stroke="#c8a84a" stroke-width="3" stroke-linecap="round"/>
      </svg>
      <div id="cc-key-num"></div>
      <div id="cc-key-name"></div>
      <div id="cc-key-msg"></div>
      <button id="cc-key-btn" onclick="CC_KEYS.dismiss()">Take the key</button>
    </div>
  `;
  document.body.appendChild(overlay);

  const ROMAN = ['I','II','III','IV','V','VI','VII'];
  const LOCATIONS = ['Headspace','Herbal Atelier','Fermentation Lab','Audio Sanctuary','The Garden','The Forest','The Corridor'];
  const MESSAGES = [
    'Frequency revealed its secret.',
    'The immortal tree gave you its mark.',
    'The firefly led you here.',
    'A smile hidden in sound.',
    'The garden shared its secret with you.',
    'The red tree recognized you.',
    'Two became one. The door opened.'
  ];

  let pendingKey = null;

  async function award(keyNum){
    if(!player){ console.warn('No player — key not awarded'); return; }
    if((player.keys||[]).includes(keyNum)){ return; } // already have it

    pendingKey = keyNum;

    // Show overlay
    document.getElementById('cc-key-num').textContent = 'Key ' + ROMAN[keyNum-1];
    document.getElementById('cc-key-name').textContent = LOCATIONS[keyNum-1];
    document.getElementById('cc-key-msg').textContent = MESSAGES[keyNum-1];
    overlay.classList.add('show');
    showing = true;
  }

  async function dismiss(){
    if(!pendingKey) return;
    overlay.classList.remove('show');
    showing = false;

    // Save to Supabase
    const newKeys = [...(player.keys||[]), pendingKey];
    player.keys = newKeys;
    localStorage.setItem('cc_player', JSON.stringify(player));

    await fetch(SUPA_URL+'/rest/v1/players?name=eq.'+encodeURIComponent(player.name), {
      method:'PATCH',
      headers:{
        'Content-Type':'application/json',
        'apikey':SUPA_KEY,
        'Authorization':'Bearer '+SUPA_KEY,
        'Prefer':'return=minimal'
      },
      body:JSON.stringify({keys_found:newKeys})
    }).catch(()=>{});

    pendingKey = null;
  }

  function hasKey(n){ return (player?.keys||[]).includes(n); }
  function isPlaying(){ return !!player; }
  function getPlayer(){ return player; }
  function keyCount(){ return (player?.keys||[]).length; }

  return { award, dismiss, hasKey, isPlaying, getPlayer, keyCount };
})();
