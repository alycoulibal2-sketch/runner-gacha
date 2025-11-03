  
<!DOCTYPE html>  
<html lang="en">  
<head>  
  <meta charset="utf-8" />  
  <title>Runner Gacha (30 coins)</title>  
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />  
  <style>  
    :root{  
      --bg-1: #071029;  
      --bg-2: #0f172a;  
      --accent: #ff7a59;  
      --accent-2: #7c4dff;  
      --text: #e6eef8;  
      --glass: rgba(255,255,255,0.06);  
      --glass-strong: rgba(255,255,255,0.09);  
    }  
  
    * { box-sizing: border-box; margin:0; padding:0; }  
    html,body{ height:100%; }  
    body {  
      background: radial-gradient(circle at top, #0b1220, var(--bg-2));  
      font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;  
      color: var(--text);  
      display:flex;  
      align-items:center;  
      justify-content:center;  
      height:100vh;  
      -webkit-font-smoothing:antialiased;  
      -moz-osx-font-smoothing:grayscale;  
      touch-action: manipulation;  
      user-select:none;  
    }  
  
    #game {  
      width: 420px;  
      max-width: 96vw;  
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));  
      border-radius: 18px;  
      box-shadow: 0 24px 60px rgba(2,6,23,0.7);  
      position: relative;  
      overflow: hidden;  
    }  
  
    canvas { display:block; border-radius:18px; width:100%; height: calc(640px * (100%/420px)); /* maintain aspect visually */ background: transparent; }  
  
    /* Top UI */  
    #ui {  
      position: absolute;  
      top: 12px;  
      left: 50%;  
      transform: translateX(-50%);  
      display:flex;  
      gap:8px;  
      z-index:20;  
      align-items:center;  
      justify-content:center;  
      flex-wrap:wrap;  
      width: calc(100% - 24px);  
      padding: 0 12px;  
    }  
    .badge {  
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.015));  
      border: 1px solid rgba(255,255,255,0.04);  
      padding: 6px 12px;  
      border-radius: 999px;  
      font-size:13px;  
      font-weight:700;  
      display:flex;  
      gap:8px;  
      align-items:center;  
      color:var(--text);  
      box-shadow: 0 4px 18px rgba(2,6,23,0.5);  
    }  
    .badge-btn{  
      background:var(--glass);  
      border: 1px solid rgba(255,255,255,0.04);  
      padding:6px 10px;  
      border-radius:999px;  
      font-weight:700;  
      cursor:pointer;  
      color:var(--text);  
      font-size:13px;  
    }  
  
    /* Menu overlay */  
    #menu {  
      position:absolute;  
      inset:0;  
      background: linear-gradient(180deg, rgba(2,6,23,0.88), rgba(2,6,23,0.98));  
      display:flex;  
      flex-direction:column;  
      align-items:center;  
      justify-content:center;  
      gap:12px;  
      z-index:30;  
      text-align:center;  
      padding:18px;  
    }  
    h1.title {  
      font-size:22px;  
      letter-spacing:0.8px;  
      margin-bottom:4px;  
    }  
    p.desc { opacity:0.8; font-size:13px; margin-bottom:6px; }  
  
    .difficulty-row { display:flex; gap:10px; flex-wrap:wrap; justify-content:center; }  
  
    .btn {  
      border:none;  
      padding:10px 16px;  
      border-radius:12px;  
      font-weight:800;  
      cursor:pointer;  
      min-width:120px;  
      transition: transform .08s, box-shadow .12s;  
      font-size:14px;  
      color:#021021;  
      box-shadow: 0 8px 30px rgba(0,0,0,0.45);  
    }  
    .btn:active{ transform: translateY(2px) scale(.996); }  
    .easy { background: #34d399; color:#021021; }  
    .hard { background: #f87171; color:#021021; }  
    .extreme { background: #8b5cf6; color:#021021; }  
    .shop { background: linear-gradient(90deg,#ffb86b,#ff7a59); color:#021021; box-shadow: 0 12px 40px rgba(255,122,89,0.12); }  
    .secondary { background: transparent; color:var(--text); border:1px solid rgba(255,255,255,0.04); padding:8px 14px; }  
  
    small.note { opacity:.7; font-size:12px; }  
  
    /* Gacha Modal */  
    #gachaModal {  
      position:absolute; inset:0;  
      background: linear-gradient(180deg, rgba(2,6,23,0.96), rgba(2,6,23,0.98));  
      display:none;  
      z-index:40;  
      align-items:center;  
      justify-content:center;  
      flex-direction:column;  
      gap:10px;  
      padding:12px;  
    }  
    .gacha-type-row { display:flex; gap:8px; }  
    .gacha-type-btn {  
      background: var(--glass);  
      border-radius:999px;  
      padding:6px 12px;  
      font-size:13px;  
      cursor:pointer;  
      border:1px solid rgba(255,255,255,0.03);  
      color:var(--text);  
      font-weight:700;  
    }  
    .gacha-type-btn.active { background: linear-gradient(90deg,#7c4dff,#ff7a59); color:#021021; }  
  
    #gachaWheel {  
      background: linear-gradient(180deg,#020617,#071a2a);  
      border-radius:50%;  
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);  
      width:240px;height:240px;  
      border: 6px solid rgba(255,255,255,0.02);  
      margin:6px 0;  
    }  
    #spinBtn {  
      padding:10px 18px;  
      border-radius:12px;  
      border:none;  
      background:linear-gradient(90deg,#ffb86b,#ff7a59);  
      color:#021021;  
      font-weight:900;  
      cursor:pointer;  
    }  
    #gachaResult { color: #cfe9ff; opacity:0.95; font-weight:700; margin-top:6px; }  
    #pityInfo { color:#a8bcd6; font-size:12px; margin-top:4px; }  
  
    /* Reward overlay */  
    #rewardFull {  
      position:absolute; inset:0;  
      background: rgba(0,0,0,0.45);  
      display:none;  
      z-index:50;  
      align-items:center;  
      justify-content:center;  
    }  
    .reward-card {  
      width:88%; max-width:420px;  
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));  
      border-radius:18px;  
      padding:16px;  
      text-align:center;  
      box-shadow: 0 24px 60px rgba(0,0,0,0.6);  
      border: 2px solid rgba(255,255,255,0.045);  
    }  
    .reward-title { font-size:13px; opacity:.9; }  
    .reward-name { font-size:20px; font-weight:900; margin:6px 0; }  
    .reward-rarity { font-weight:900; margin-bottom:8px; }  
    .reward-type { opacity:.7; margin-bottom:10px; }  
    .reward-actions { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }  
    .reward-btn { border:none; padding:8px 12px; border-radius:12px; font-weight:700; cursor:pointer; }  
  
    .bg-common     { background: linear-gradient(180deg,#0f172a,#07102a); }  
    .bg-rare       { background: linear-gradient(180deg,#38bdf8,#07102a); color:#021021; }  
    .bg-epic       { background: linear-gradient(180deg,#a855f7,#07102a); }  
    .bg-legendaire { background: linear-gradient(180deg,#ffb86b,#07102a); color:#021021; }  
    .bg-mythic     { background: linear-gradient(180deg,#ff6b94,#07102a); }  
  
    /* Collection */  
    #collectionModal {  
      position:absolute; inset:0;  
      background: linear-gradient(180deg, rgba(2,6,23,0.98), rgba(2,6,23,0.995));  
      display:none;  
      z-index:60;  
      flex-direction:column;  
      padding:12px;  
      gap:10px;  
      overflow:hidden;  
    }  
    #collectionModal h2 { text-align:center; }  
    .collection-tabs { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }  
    .collection-tab { background:var(--glass); padding:6px 10px; border-radius:999px; border:1px solid rgba(255,255,255,0.03); cursor:pointer; font-weight:700; color:var(--text); }  
    .collection-tab.active { background: linear-gradient(90deg,#7c4dff,#ff7a59); color:#021021; }  
  
    .collection-body-scroll { flex:1; overflow:auto; padding:6px 4px; }  
    .collection-section-title { font-size:12px; opacity:.7; margin:4px 0 6px; }  
    .collection-type-block { display:grid; grid-template-columns: repeat(auto-fill, minmax(95px,1fr)); gap:10px; margin-bottom:10px; }  
  
    .skin-card { background: rgba(255,255,255,0.02); border-radius:12px; padding:8px; height:110px; display:flex; flex-direction:column; justify-content:space-between; align-items:center; font-size:12px; border:1px solid rgba(255,255,255,0.02); }  
    .skin-box { width:60px; height:45px; border-radius:10px; background: rgba(255,255,255,0.03); }  
    .skin-name { font-weight:700; font-size:12px; text-align:center; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; width:100%; }  
    .skin-type { font-size:11px; opacity:.6; }  
    .equip-btn { border:none; background:#34d399; color:#021021; padding:6px 10px; border-radius:999px; font-weight:800; cursor:pointer; font-size:12px; }  
  
    .locked { filter:grayscale(1) brightness(.3); position:relative; }  
    .locked::after { content:"?"; position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:18px; color:rgba(255,255,255,0.25); pointer-events:none; }  
  
    .collection-close { align-self:center; background:var(--glass); border-radius:999px; padding:8px 14px; border:1px solid rgba(255,255,255,0.03); cursor:pointer; }  
  
    /* Bottom right quick buttons */  
    #quickButtons {  
      position:absolute; right:14px; bottom:12px; z-index:22; display:flex; gap:8px; flex-direction:column;  
    }  
    .quick {  
      background: var(--glass);  
      padding:8px 10px;  
      border-radius:999px;  
      border:1px solid rgba(255,255,255,0.03);  
      font-weight:800;  
      cursor:pointer;  
      color:var(--text);  
      display:flex;  
      gap:8px;  
      align-items:center;  
    }  
  
    /* small touches */  
    .muted { opacity:.7; font-size:12px; }  
    .hidden { display:none; }  
  
    /* responsive */  
    @media (max-width:500px){  
      #game { width:100vw; height:80vh; border-radius:0; }  
      canvas { height: calc(100% - 0px); }  
      .btn { min-width: 92px; padding:8px 10px; }  
      #gachaWheel { width:200px;height:200px; }  
    }  
  </style>  
</head>  
<body>  
  <div id="game">  
    <canvas id="canvas" width="420" height="640"></canvas>  
  
    <div id="ui">  
      <div class="badge">Score: <span id="score">0</span></div>  
      <div class="badge">Best: <span id="best">0</span></div>  
      <div class="badge">Mode: <span id="modeLabel">-</span></div>  
      <div class="badge">💰 <span id="coinAmount">0</span></div>  
      <button class="badge-btn" onclick="openCollection()" title="Open Collection">📦</button>  
      <button class="badge-btn" id="pauseBtn" onclick="togglePause()" title="Pause / Resume">⏸</button>  
      <button class="badge-btn" id="soundBtn" onclick="toggleSound()" title="Toggle sound">🔊</button>  
    </div>  
  
    <div id="menu">  
      <h1 class="title">Runner Gacha</h1>  
      <p class="desc">Choose a difficulty and run as far as you can — spin the wheel to unlock skins!</p>  
  
      <div class="difficulty-row">  
        <button class="btn easy" onclick="selectDifficulty('easy')">Easy</button>  
        <button class="btn hard" onclick="selectDifficulty('hard')">Hard</button>  
        <button class="btn extreme" onclick="selectDifficulty('extreme')">Extreme</button>  
      </div>  
  
      <div style="display:flex; gap:8px; margin-top:6px; flex-wrap:wrap; justify-content:center;">  
        <button class="btn shop" onclick="openGacha()">🎰 Wheel & Skins</button>  
        <button class="btn secondary" onclick="openCollection()">📦 Collection</button>  
      </div>  
  
      <div style="display:flex; gap:8px; margin-top:8px; align-items:center;">  
        <button class="btn secondary" onclick="claimDaily()" id="dailyBtn">🎁 Daily Reward</button>  
        <small class="note">1 spin = 30 💰 • 50 spins = guaranteed legendary</small>  
      </div>  
  
      <small class="muted">Controls: tap or space to jump. P = pause, G = gacha, C = collection</small>  
    </div>  
  
    <div id="gachaModal">  
      <h2 style="margin:0;">🎰 Gacha Wheel</h2>  
      <div id="gachaCoins" class="muted">Your coins: 0</div>  
  
      <div class="gacha-type-row" style="margin-top:6px;">  
        <button class="gacha-type-btn active" data-type="player" onclick="selectGachaType('player', this)">Player</button>  
        <button class="gacha-type-btn" data-type="background" onclick="selectGachaType('background', this)">Background</button>  
        <button class="gacha-type-btn" data-type="obstacle" onclick="selectGachaType('obstacle', this)">Obstacle</button>  
      </div>  
  
      <canvas id="gachaWheel" width="240" height="240"></canvas>  
  
      <div style="display:flex; gap:8px; align-items:center; margin-top:6px; flex-wrap:wrap; justify-content:center;">  
        <button class="btn shop" id="spinBtn">Spin (30 💰)</button>  
        <button class="btn secondary" onclick="closeGacha()">Close</button>  
      </div>  
  
      <div id="gachaResult">Spin to get new skins!</div>  
      <small id="pityInfo" class="muted"></small>  
    </div>  
  
    <div id="rewardFull">  
      <div id="rewardCard" class="reward-card">  
        <div class="reward-title">NEW SKIN</div>  
        <div id="rewardName" class="reward-name">Skin name</div>  
        <div id="rewardRarity" class="reward-rarity">RARITY</div>  
        <div id="rewardType" class="reward-type">Type</div>  
        <div class="reward-actions">  
          <button class="reward-btn" id="btnEquip">Equip</button>  
          <button class="reward-btn" id="btnCollection">Open Collection</button>  
          <button class="reward-btn" id="btnCloseReward">Close</button>  
        </div>  
      </div>  
    </div>  
  
    <div id="collectionModal">  
      <h2>📦 Collection</h2>  
      <div class="collection-tabs">  
        <button class="collection-tab active" onclick="showCollection('all', this)">All</button>  
        <button class="collection-tab" onclick="showCollection('commun', this)">Common</button>  
        <button class="collection-tab" onclick="showCollection('rare', this)">Rare</button>  
        <button class="collection-tab" onclick="showCollection('epic', this)">Epic</button>  
        <button class="collection-tab" onclick="showCollection('legendaire', this)">Legendary</button>  
        <button class="collection-tab" onclick="showCollection('mythique', this)">Mythic</button>  
      </div>  
  
      <div id="collectionBody" class="collection-body-scroll"></div>  
      <button class="collection-close" onclick="closeCollection()">Close</button>  
    </div>  
  
    <div id="quickButtons">  
      <button class="quick" onclick="openGacha()" title="Open Gacha">🎰 Wheel</button>  
      <button class="quick" onclick="openCollection()" title="Open Collection">📦 Collection</button>  
    </div>  
  </div>  
  
  <script>  
    // ======= Core canvas and basic game vars =======  
    const canvas = document.getElementById("canvas");  
    const ctx = canvas.getContext("2d");  
  
    const scoreEl = document.getElementById("score");  
    const bestEl = document.getElementById("best");  
    const modeLabel = document.getElementById("modeLabel");  
    const coinAmountEl = document.getElementById("coinAmount");  
    const menu = document.getElementById("menu");  
    const gachaModal = document.getElementById("gachaModal");  
    const gachaCoins = document.getElementById("gachaCoins");  
    const gachaResult = document.getElementById("gachaResult");  
    const pityInfo = document.getElementById("pityInfo");  
    const rewardFull = document.getElementById("rewardFull");  
    const rewardCard = document.getElementById("rewardCard");  
    const rewardNameEl = document.getElementById("rewardName");  
    const rewardRarityEl = document.getElementById("rewardRarity");  
    const rewardTypeEl = document.getElementById("rewardType");  
    const btnEquip = document.getElementById("btnEquip");  
    const btnCollection = document.getElementById("btnCollection");  
    const btnCloseReward = document.getElementById("btnCloseReward");  
    const collectionModal = document.getElementById("collectionModal");  
    const collectionBody = document.getElementById("collectionBody");  
    const pauseBtn = document.getElementById("pauseBtn");  
    const soundBtn = document.getElementById("soundBtn");  
    const dailyBtn = document.getElementById("dailyBtn");  
  
    // Keep canvas pixel size fixed; CSS scales it visually  
    const w = canvas.width;  
    const h = canvas.height;  
    const groundY = h - 80;  
  
    const player = { x:70, y: h - 140, w:50, h:50, vy:0, onGround:true };  
  
    const DIFFICULTIES = {  
      easy:   { name: "Easy",       color: "#34d399", startSpeed: 2.2, accel: 0.02, coinValue: 1, spawnBase: 180 },  
      hard:   { name: "Hard",       color: "#f87171", startSpeed: 3.2, accel: 0.045, coinValue: 2, spawnBase: 140 },  
      extreme:{ name: "Extreme",    color: "#8b5cf6", startSpeed: 4.0, accel: 0.08, coinValue: 3, spawnBase: 110 },  
    };  
  
    const FIXED_SPAWN_FRAMES = 180;  
    const COIN_SPAWN_FRAMES = 110;  
  
    let currentDiff = null;  
    let obstacles = [];  
    let coinsOnField = [];  
    let gameSpeed = 3;  
    let score = 0;  
    let best = Number(localStorage.getItem("rg-best") || 0);  
    bestEl.textContent = best;  
    let coins = Number(localStorage.getItem("rg-coins") || 0);  
    coinAmountEl.textContent = coins;  
    let spawnTimer = FIXED_SPAWN_FRAMES;  
    let coinSpawnTimer = COIN_SPAWN_FRAMES;  
    let running = false;  
    let menuOpen = true;  
    let paused = false;  
  
    // daily reward tracking  
    let lastDaily = Number(localStorage.getItem("rg-lastDaily") || 0);  
  
    // skins - original set translated to english  
    const SKINS = [  
      // 20 COMMON  
      {name:"Green Block", rarity:"commun", type:"player"},  
      {name:"Blue Block", rarity:"commun", type:"player"},  
      {name:"Red Block", rarity:"commun", type:"player"},  
      {name:"Grey Block", rarity:"commun", type:"player"},  
      {name:"Orange Block", rarity:"commun", type:"player"},  
      {name:"Mint Block", rarity:"commun", type:"player"},  
      {name:"Pastel Block", rarity:"commun", type:"player"},  
      {name:"Sand Block", rarity:"commun", type:"player"},  
      {name:"Simple Background", rarity:"commun", type:"background"},  
      {name:"Grey Background", rarity:"commun", type:"background"},  
      {name:"Midnight Blue Background", rarity:"commun", type:"background"},  
      {name:"Concrete Background", rarity:"commun", type:"background"},  
      {name:"Thin Lines Background", rarity:"commun", type:"background"},  
      {name:"Soft Clouds Background", rarity:"commun", type:"background"},  
      {name:"Soft Tiles Background", rarity:"commun", type:"background"},  
      {name:"Red Obstacle", rarity:"commun", type:"obstacle"},  
      {name:"Grey Obstacle", rarity:"commun", type:"obstacle"},  
      {name:"Light Obstacle", rarity:"commun", type:"obstacle"},  
      {name:"Wood Obstacle", rarity:"commun", type:"obstacle"},  
      {name:"Simple Light Obstacle", rarity:"commun", type:"obstacle"},  
  
      // 20 RARE  
      {name:"Sky Stripes Block", rarity:"rare", type:"player"},  
      {name:"Diagonal Block", rarity:"rare", type:"player"},  
      {name:"Tech Light Block", rarity:"rare", type:"player"},  
      {name:"Blue Edge Block", rarity:"rare", type:"player"},  
      {name:"City Block", rarity:"rare", type:"player"},  
      {name:"Edge Block", rarity:"rare", type:"player"},  
      {name:"Blue Gradient Block", rarity:"rare", type:"player"},  
      {name:"Tiles Background", rarity:"rare", type:"background"},  
      {name:"Blue Lines Background", rarity:"rare", type:"background"},  
      {name:"Blue Stripes Background", rarity:"rare", type:"background"},  
      {name:"Waves Background", rarity:"rare", type:"background"},  
      {name:"Soft Violet Background", rarity:"rare", type:"background"},  
      {name:"City Dusk Background", rarity:"rare", type:"background"},  
      {name:"Holo Background", rarity:"rare", type:"background"},  
      {name:"Carbon Obstacle", rarity:"rare", type:"obstacle"},  
      {name:"Sheet Metal Obstacle", rarity:"rare", type:"obstacle"},  
      {name:"Cyan Obstacle", rarity:"rare", type:"obstacle"},  
      {name:"Tiled Obstacle", rarity:"rare", type:"obstacle"},  
      {name:"Rust Obstacle", rarity:"rare", type:"obstacle"},  
      {name:"Grill Obstacle", rarity:"rare", type:"obstacle"},  
  
      // 15 EPIC  
      {name:"Galaxy Dots", rarity:"epic", type:"background"},  
      {name:"Neon Lines", rarity:"epic", type:"background"},  
      {name:"Laser Background", rarity:"epic", type:"background"},  
      {name:"Nebula Background", rarity:"epic", type:"background"},  
      {name:"Holo Waves Background", rarity:"epic", type:"background"},  
      {name:"Techno Background", rarity:"epic", type:"background"},  
      {name:"Neon Block", rarity:"epic", type:"player"},  
      {name:"Techno Block", rarity:"epic", type:"player"},  
      {name:"Prism Block", rarity:"epic", type:"player"},  
      {name:"Pastel Neon Block", rarity:"epic", type:"player"},  
      {name:"Shimmer Block", rarity:"epic", type:"player"},  
      {name:"Violet Lines Obstacle", rarity:"epic", type:"obstacle"},  
      {name:"Prism Obstacle", rarity:"epic", type:"obstacle"},  
      {name:"Neon Grid Obstacle", rarity:"epic", type:"obstacle"},  
      {name:"Crystal Blue Obstacle", rarity:"epic", type:"obstacle"},  
  
      // 10 LEGENDARY  
      {name:"Gold Lines Block", rarity:"legendaire", type:"player"},  
      {name:"Flame Block", rarity:"legendaire", type:"player"},  
      {name:"Magma Block", rarity:"legendaire", type:"player"},  
      {name:"Brushed Gold Block", rarity:"legendaire", type:"player"},  
      {name:"Cyber Dusk Background", rarity:"legendaire", type:"background"},  
      {name:"Solar Temple Background", rarity:"legendaire", type:"background"},  
      {name:"Neon Sunset Background", rarity:"legendaire", type:"background"},  
      {name:"Gold Pattern Obstacle", rarity:"legendaire", type:"obstacle"},  
      {name:"Pharaoh Obstacle", rarity:"legendaire", type:"obstacle"},  
      {name:"Royal Obstacle", rarity:"legendaire", type:"obstacle"},  
  
      // 5 MYTHIC  
      {name:"Bananas Block", rarity:"mythique", type:"player"},  
      {name:"Mythic Runes Block", rarity:"mythique", type:"player"},  
      {name:"Sky Bananas Background", rarity:"mythique", type:"background"},  
      {name:"Mythic Portal Background", rarity:"mythique", type:"background"},  
      {name:"Crystal Obstacle", rarity:"mythique", type:"obstacle"},  
    ];  
  
    // Owned selected and pity stored  
    let ownedSkins = JSON.parse(localStorage.getItem("rg-skins") || '{"background":[],"player":[],"obstacle":[]}');  
    let selectedSkins = JSON.parse(localStorage.getItem("rg-selected") || '{"background":"default","player":"default","obstacle":"default"}');  
    let pity = JSON.parse(localStorage.getItem("rg-pity") || '{"background":0,"player":0,"obstacle":0}');  
  
    // audio (simple)  
    let audioEnabled = (localStorage.getItem("rg-sound") !== "false");  
    updateSoundUI();  
    let audioCtx;  
    function ensureAudioCtx(){  
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();  
    }  
    function playBeep(freq=440, time=0.06, type='sine', vol=0.05){  
      if (!audioEnabled) return;  
      ensureAudioCtx();  
      const o = audioCtx.createOscillator();  
      const g = audioCtx.createGain();  
      o.type = type;  
      o.frequency.value = freq;  
      g.gain.value = vol;  
      o.connect(g); g.connect(audioCtx.destination);  
      o.start();  
      o.stop(audioCtx.currentTime + time);  
    }  
    function updateSoundUI(){  
      soundBtn.textContent = audioEnabled ? '🔊' : '🔈';  
      localStorage.setItem("rg-sound", audioEnabled ? "true" : "false");  
    }  
    function toggleSound(){  
      audioEnabled = !audioEnabled;  
      updateSoundUI();  
      playBeep(880,0.08);  
    }  
  
    function saveAll(){  
      localStorage.setItem("rg-coins", coins);  
      localStorage.setItem("rg-best", best);  
      localStorage.setItem("rg-skins", JSON.stringify(ownedSkins));  
      localStorage.setItem("rg-selected", JSON.stringify(selectedSkins));  
      localStorage.setItem("rg-pity", JSON.stringify(pity));  
    }  
  
    // Create pattern previews for skins - simple procedural patterns  
    function makePattern(name){  
      const c = document.createElement("canvas");  
      const size = 80;  
      c.width = size; c.height = size;  
      const p = c.getContext("2d");  
      if (!name) return null;  
      const fillAll = col => { p.fillStyle=col; p.fillRect(0,0,size,size); };  
  
      // small selection of visuals  
      if (name.includes("Background") || name.includes("background") || name.toLowerCase().includes("sky") || name.toLowerCase().includes("nebula")){  
        // gradient backgrounds  
        const g = p.createLinearGradient(0,0,size,size);  
        g.addColorStop(0, "#07102a");  
        g.addColorStop(1, "#0f172a");  
        p.fillStyle = g; p.fillRect(0,0,size,size);  
        p.fillStyle = "rgba(255,255,255,0.02)";  
        for (let i=0;i<8;i++){ p.beginPath(); p.arc(Math.random()*size, Math.random()*size, Math.random()*6, 0, Math.PI*2); p.fill();}  
      } else if (name.toLowerCase().includes("block") || name.toLowerCase().includes("bloc") || name.toLowerCase().includes("bananas")){  
        // block - solid or stripes  
        if (name.toLowerCase().includes("green")) fillAll("#34d399");  
        else if (name.toLowerCase().includes("blue")) fillAll("#38bdf8");  
        else if (name.toLowerCase().includes("red")) fillAll("#ef4444");  
        else if (name.toLowerCase().includes("gold") || name.toLowerCase().includes("brushed")) fillAll("#ffb86b");  
        else if (name.toLowerCase().includes("magma") || name.toLowerCase().includes("flame")) fillAll("#7f1d1d");  
        else if (name.toLowerCase().includes("bananas")) { fillAll("#fef08a"); p.fillStyle="#d97706"; p.fillRect(6,8,8,18); p.fillRect(28,12,8,18); p.fillRect(48,6,8,18); }  
        else fillAll("#0f172a");  
  
        if (name.toLowerCase().includes("stripes") || name.toLowerCase().includes("strip") || name.toLowerCase().includes("stripes block")){  
          p.strokeStyle="rgba(255,255,255,0.08)"; p.lineWidth=4;  
          for (let i=0;i<size;i+=10){ p.beginPath(); p.moveTo(i,0); p.lineTo(i,size); p.stroke(); }  
        }  
      } else if (name.toLowerCase().includes("obstacle") || name.toLowerCase().includes("obst")) {  
        // obstacles - darker  
        fillAll("#1f2937");  
        p.fillStyle = "rgba(255,255,255,0.03)";  
        for (let y=6;y<size;y+=12){ p.fillRect(6,y, size-12, 6); }  
      } else {  
        // default  
        fillAll("#0f172a");  
      }  
  
      return p.createPattern(c,"repeat");  
    }  
  
    // ===== Game functions =====  
    function selectDifficulty(mode){  
      currentDiff = DIFFICULTIES[mode];  
      modeLabel.textContent = currentDiff.name;  
      startGame();  
    }  
  
    function startGame(){  
      obstacles = [];  
      coinsOnField = [];  
      gameSpeed = currentDiff.startSpeed;  
      score = 0;  
      player.y = groundY - player.h;  
      player.vy = 0;  
      player.onGround = true;  
      spawnTimer = currentDiff.spawnBase || FIXED_SPAWN_FRAMES;  
      coinSpawnTimer = COIN_SPAWN_FRAMES;  
      scoreEl.textContent = score;  
      running = true;  
      paused = false;  
      menu.style.display = "none";  
      gachaModal.style.display = "none";  
      collectionModal.style.display = "none";  
      menuOpen = false;  
      playBeep(880,0.06);  
      requestAnimationFrame(gameLoop);  
    }  
  
    function gameOver(){  
      running = false;  
      menu.style.display = "flex";  
      menuOpen = true;  
      if (score > best){  
        best = score;  
        bestEl.textContent = best;  
        // celebratory beep  
        playBeep(1400,0.18,'sine',0.07);  
      } else {  
        playBeep(220,0.08);  
      }  
      saveAll();  
    }  
  
    function spawnObstacle(){  
      const hObs = 40 + Math.random()*55;  
      obstacles.push({ x: w + 50 + Math.random()*80, y: groundY - hObs, w: 50 + Math.random()*20, h: hObs, passed:false, id:Math.random().toString(36).slice(2) });  
    }  
  
    function spawnCoin(){  
      coinsOnField.push({ x: w + 30 + Math.random()*40, y: groundY - 40 - Math.random()*60, r: 12, taken:false, id:Math.random().toString(36).slice(2) });  
    }  
  
    function jump(){  
      if (running && !paused && player.onGround){  
        player.vy = -13;  
        player.onGround = false;  
        playBeep(880,0.06);  
      }  
    }  
  
    // Improvement: smoother obstacle spawn distribution and difficulty curve  
    function gameLoop(){  
      if (!running) return;  
      if (paused){ requestAnimationFrame(gameLoop); return; }  
  
      // background  
      let bgPattern = null;  
      if (selectedSkins.background !== "default") bgPattern = makePattern(selectedSkins.background);  
      ctx.fillStyle = bgPattern ? bgPattern : "#020617";  
      ctx.fillRect(0,0,w,h);  
  
      // ground  
      ctx.fillStyle = "rgba(15,23,42,0.44)";  
      ctx.fillRect(0, groundY, w, h - groundY);  
  
      // physics  
      player.vy += 0.36;  
      if (player.vy > 9) player.vy = 9;  
      player.y += player.vy;  
      if (player.y + player.h >= groundY){  
        player.y = groundY - player.h;  
        player.vy = 0;  
        player.onGround = true;  
      }  
  
      // player draw  
      let playerPat = null;  
      if (selectedSkins.player !== "default") playerPat = makePattern(selectedSkins.player);  
      ctx.fillStyle = playerPat ? playerPat : (currentDiff ? currentDiff.color : "#38bdf8");  
      ctx.fillRect(player.x, Math.round(player.y), player.w, player.h);  
  
      // spawn obstacles  
      spawnTimer--;  
      if (spawnTimer <= 0){  
        spawnObstacle();  
        // spawn frequency scales with speed and difficulty  
        const variance = Math.max(60, Math.floor((200 - gameSpeed*20) + Math.random()*40));  
        spawnTimer = (currentDiff.spawnBase || FIXED_SPAWN_FRAMES) - Math.floor(gameSpeed*6) + Math.floor(Math.random()*variance);  
      }  
  
      // obstacles update  
      for (let i=obstacles.length-1;i>=0;i--){  
        const ob = obstacles[i];  
        ob.x -= gameSpeed;  
        let obPat = null;  
        if (selectedSkins.obstacle !== "default") obPat = makePattern(selectedSkins.obstacle);  
        ctx.fillStyle = obPat ? obPat : "#f43f5e";  
        ctx.fillRect(ob.x, ob.y, ob.w, ob.h);  
  
        // collision  
        if (player.x < ob.x + ob.w &&  
            player.x + player.w > ob.x &&  
            player.y < ob.y + ob.h &&  
            player.y + player.h > ob.y){  
          gameOver();  
        }  
  
        // passed  
        if (!ob.passed && ob.x + ob.w < player.x){  
          ob.passed = true;  
          score++;  
          scoreEl.textContent = score;  
          gameSpeed += currentDiff.accel; // gradually accelerate  
        }  
  
        // cleanup  
        if (ob.x + ob.w < -60) obstacles.splice(i,1);  
      }  
  
      // coins spawn and update  
      coinSpawnTimer--;  
      if (coinSpawnTimer <= 0){  
        spawnCoin();  
        coinSpawnTimer = COIN_SPAWN_FRAMES + Math.floor(Math.random()*60);  
      }  
  
      for (let i=coinsOnField.length-1;i>=0;i--){  
        const c = coinsOnField[i];  
        c.x -= gameSpeed;  
        if (!c.taken){  
          // coin shine animation  
          const yOff = Math.sin((Date.now()+i*50)/200) * 2;  
          ctx.beginPath();  
          ctx.fillStyle = "#facc15";  
          ctx.arc(c.x, c.y + yOff, c.r, 0, Math.PI*2);  
          ctx.fill();  
        }  
  
        if (!c.taken &&  
            player.x < c.x + c.r &&  
            player.x + player.w > c.x - c.r &&  
            player.y < c.y + c.r &&  
            player.y + player.h > c.y - c.r){  
          c.taken = true;  
          const gain = currentDiff ? currentDiff.coinValue : 1;  
          coins += gain;  
          // coin pickup animation: small float text  
          animateFloatingText("+" + gain, c.x, c.y, "#facc15");  
          coinAmountEl.textContent = coins;  
          saveAll();  
          playBeep(1100,0.06,'sine',0.05);  
        }  
  
        if (c.x + c.r < -60 || c.taken) coinsOnField.splice(i,1);  
      }  
  
      // loop  
      requestAnimationFrame(gameLoop);  
    }  
  
    // floating text helper  
    function animateFloatingText(text, sx, sy, color="#fff"){  
      const duration = 800;  
      const start = performance.now();  
      function frame(now){  
        const t = (now - start) / duration;  
        if (t >= 1) return;  
        const alpha = 1 - t;  
        const y = sy - (t * 30);  
        ctx.save();  
        ctx.font = "bold 16px system-ui";  
        ctx.fillStyle = color;  
        ctx.globalAlpha = alpha;  
        ctx.fillText(text, sx-10, y);  
        ctx.restore();  
        requestAnimationFrame(frame);  
      }  
      requestAnimationFrame(frame);  
    }  
  
    // ===== Gacha logic (30 coins, pity system, translated to English) =====  
    const gachaCanvas = document.getElementById("gachaWheel");  
    const gctx = gachaCanvas.getContext("2d");  
    const R = gachaCanvas.width / 2;  
  
    const wheelSegments = [  
      { label: "Common",    color: "#94a3b8", rarity: "commun" },  
      { label: "Rare",      color: "#38bdf8", rarity: "rare" },  
      { label: "Epic",      color: "#a855f7", rarity: "epic" },  
      { label: "Legendary", color: "#ffb86b", rarity: "legendaire" },  
      { label: "Mythic",    color: "#ff6b94", rarity: "mythique" },  
    ];  
  
    let wheelRotation = 0;  
    let wheelSpinning = false;  
    let wheelStartDeg = 0;  
    let wheelTargetDeg = 0;  
    let wheelStartTime = 0;  
    let wheelDuration = 1800;  
    let currentWheelType = "player";  
    let forcedRarity = null;  
    let currentSpinRarity = null;  
  
    function drawWheel(rotDeg=0){  
      gctx.clearRect(0,0,gachaCanvas.width,gachaCanvas.height);  
      const total = wheelSegments.length;  
      const step = (2*Math.PI)/total;  
  
      gctx.save();  
      gctx.translate(R,R);  
      gctx.rotate(rotDeg*Math.PI/180);  
  
      for (let i=0;i<total;i++){  
        const start = i*step;  
        const end = start+step;  
        gctx.beginPath();  
        gctx.moveTo(0,0);  
        gctx.arc(0,0,R,start,end);  
        gctx.fillStyle = wheelSegments[i].color;  
        gctx.fill();  
  
        gctx.save();  
        gctx.rotate(start+step/2);  
        gctx.fillStyle = "#021021";  
        gctx.font = "700 12px system-ui";  
        gctx.textAlign = "right";  
        gctx.fillText(wheelSegments[i].label, R-12, 6);  
        gctx.restore();  
      }  
  
      gctx.restore();  
  
      // pointer on right  
      gctx.beginPath();  
      gctx.moveTo(gachaCanvas.width, R);  
      gctx.lineTo(gachaCanvas.width - 22, R - 16);  
      gctx.lineTo(gachaCanvas.width - 22, R + 16);  
      gctx.closePath();  
      gctx.fillStyle = "#fff";  
      gctx.fill();  
    }  
    drawWheel(0);  
  
    function openGacha(){  
      gachaModal.style.display = "flex";  
      menuOpen = true;  
      gachaCoins.textContent = "Your coins: " + coins;  
      updatePityText();  
    }  
    function closeGacha(){ gachaModal.style.display = "none"; }  
  
    function updatePityText(){  
      pityInfo.textContent = `Pity: background ${pity.background||0} | player ${pity.player||0} | obstacle ${pity.obstacle||0} (50 = guaranteed Legendary)`;  
    }  
  
    function selectGachaType(type, btn){  
      currentWheelType = type;  
      document.querySelectorAll(".gacha-type-btn").forEach(b=>b.classList.remove("active"));  
      if (btn) btn.classList.add("active");  
    }  
  
    function getAngleForRarity(rarity){  
      const idx = wheelSegments.findIndex(s=>s.rarity===rarity);  
      const slice = 360 / wheelSegments.length;  
      return idx * slice + slice/2;  
    }  
  
    // chances  
    function rollRarity(){  
      const r = Math.random();  
      if (r < 0.01) return "mythique";          // 1%  
      if (r < 0.0266667) return "legendaire";   // ~1.66%  
      if (r < 0.1166667) return "epic";         // 9%  
      if (r < 0.3966667) return "rare";         // 28%  
      return "commun";  
    }  
  
    function spinWheel(){  
      if (wheelSpinning) return;  
      if (coins < 30){  
        gachaResult.textContent = "Not enough coins 😅";  
        playBeep(220,0.07,'sine',0.04);  
        return;  
      }  
  
      coins -= 30;  
      coinAmountEl.textContent = coins;  
      gachaCoins.textContent = "Your coins: " + coins;  
  
      // increment pity  
      pity[currentWheelType] = (pity[currentWheelType] || 0) + 1;  
      forcedRarity = null;  
      currentSpinRarity = null;  
  
      if (pity[currentWheelType] >= 50) {  
        currentSpinRarity = "legendaire";  
        forcedRarity = "legendaire";  
        pity[currentWheelType] = 0;  
      } else {  
        currentSpinRarity = rollRarity();  
      }  
  
      // target angle mapping  
      const targetAngle = getAngleForRarity(currentSpinRarity);  
      const spinTo = 360 - targetAngle;  
  
      wheelStartDeg = wheelRotation % 360;  
      wheelTargetDeg = 360 * (3 + Math.floor(Math.random()*3)) + spinTo + (Math.random()*20 - 10); // more spins = more spectacular  
      wheelStartTime = performance.now();  
      wheelSpinning = true;  
  
      saveAll();  
      updatePityText();  
      playBeep(900,0.12,'sine',0.06);  
      requestAnimationFrame(animateWheel);  
    }  
  
    function animateWheel(now){  
      if (!wheelSpinning) return;  
      const elapsed = now - wheelStartTime;  
      const t = Math.min(1, elapsed / wheelDuration);  
      // smooth ease out  
      const eased = 1 - Math.pow(1 - t, 3);  
      wheelRotation = wheelStartDeg + (wheelTargetDeg - wheelStartDeg) * eased;  
      drawWheel(wheelRotation);  
      // subtle wobble sound near end  
      if (t > 0.8 && t < 0.86) playBeep(1200,0.03,'square',0.04);  
      if (t >= 1){  
        wheelSpinning = false;  
        finishSpin();  
        return;  
      }  
      requestAnimationFrame(animateWheel);  
    }  
  
    function finishSpin(){  
      let finalRot = wheelRotation % 360;  
      if (finalRot < 0) finalRot += 360;  
      const segSize = 360 / wheelSegments.length;  
      const pointerAngle = (360 - finalRot + 0.5) % 360;  
      const segIndex = Math.floor(pointerAngle / segSize) % wheelSegments.length;  
      const seg = wheelSegments[segIndex];  
      const finalRarity = (typeof forcedRarity === "string" && forcedRarity) ? forcedRarity : (currentSpinRarity || seg.rarity);  
      giveReward(finalRarity);  
    }  
  
    function giveReward(rarity){  
      let pool = SKINS.filter(s => s.rarity === rarity && s.type === currentWheelType);  
      if (pool.length === 0){  
        pool = SKINS.filter(s => s.rarity === rarity);  
      }  
      const chosen = pool[Math.floor(Math.random()*pool.length)];  
      if (!ownedSkins[chosen.type].includes(chosen.name)){  
        ownedSkins[chosen.type].push(chosen.name);  
      }  
      saveAll();  
      showReward(chosen, chosen.type);  
      playBeep(rarity === "mythique" ? 1900 : rarity === "legendaire" ? 1400 : 900, 0.18, 'sine', 0.08);  
    }  
  
    function showReward(skin, type){  
      rewardNameEl.textContent = skin.name;  
      rewardRarityEl.textContent = skin.rarity.toUpperCase();  
      rewardTypeEl.textContent = "Type: " + (type === "player" ? "Player" : type === "background" ? "Background" : "Obstacle");  
  
      rewardCard.classList.remove("bg-common","bg-rare","bg-epic","bg-legendaire","bg-mythic");  
      if (skin.rarity === "commun") rewardCard.classList.add("bg-common");  
      else if (skin.rarity === "rare") rewardCard.classList.add("bg-rare");  
      else if (skin.rarity === "epic") rewardCard.classList.add("bg-epic");  
      else if (skin.rarity === "legendaire") rewardCard.classList.add("bg-legendaire");  
      else if (skin.rarity === "mythique") rewardCard.classList.add("bg-mythic");  
  
      btnEquip.onclick = () => {  
        selectedSkins[type] = skin.name;  
        saveAll();  
        rewardFull.style.display = "none";  
      };  
      btnCollection.onclick = () => {  
        rewardFull.style.display = "none";  
        openCollection();  
        showCollection(skin.rarity);  
      };  
      btnCloseReward.onclick = () => {  
        rewardFull.style.display = "none";  
      };  
  
      rewardFull.style.display = "flex";  
    }  
  
    // ===== Collection UI =====  
    function openCollection(){  
      collectionModal.style.display = "flex";  
      menuOpen = true;  
      showCollection('all');  
    }  
    function closeCollection(){ collectionModal.style.display = "none"; }  
  
    function buildSkinCard(skin, rarityFilter){  
      const card = document.createElement("div");  
      card.className = "skin-card";  
  
      const box = document.createElement("div");  
      box.className = "skin-box";  
      const have = ownedSkins[skin.type].includes(skin.name);  
      if (have){  
        const colorByR = {  
          "commun":"#1f2937",  
          "rare":"#38bdf8",  
          "epic":"#a855f7",  
          "legendaire":"#ffb86b",  
          "mythique":"#ff6b94"  
        };  
        box.style.background = colorByR[skin.rarity] || "#1f2937";  
      } else {  
        box.classList.add("locked");  
      }  
  
      const name = document.createElement("div");  
      name.className = "skin-name";  
      name.textContent = skin.name;  
  
      const type = document.createElement("div");  
      type.className = "skin-type";  
      type.textContent = skin.type === "player" ? "Player" : (skin.type === "background" ? "Background" : "Obstacle");  
  
      card.appendChild(box);  
      card.appendChild(name);  
      card.appendChild(type);  
  
      if (have){  
        const eq = document.createElement("button");  
        eq.className = "equip-btn";  
        eq.textContent = (selectedSkins[skin.type] === skin.name) ? "Equipped" : "Equip";  
        eq.onclick = () => {  
          selectedSkins[skin.type] = skin.name;  
          saveAll();  
          showCollection(rarityFilter);  
        };  
        card.appendChild(eq);  
      } else {  
        const miss = document.createElement("div");  
        miss.style.opacity = ".45";  
        miss.style.fontSize = "11px";  
        miss.textContent = "Locked";  
        card.appendChild(miss);  
      }  
  
      return card;  
    }  
  
    function showCollection(rarity='all', btn=null){  
      if (btn){  
        document.querySelectorAll(".collection-tab").forEach(b=>b.classList.remove("active"));  
        btn.classList.add("active");  
      } else {  
        document.querySelectorAll(".collection-tab").forEach(b=>{  
          const text = b.textContent.toLowerCase();  
          if (rarity === 'all' && text === "all") b.classList.add("active");  
          else if (text.includes(rarity)) b.classList.add("active");  
          else b.classList.remove("active");  
        });  
      }  
  
      collectionBody.innerHTML = "";  
  
      const types = [  
        {id:"player", label:"🟦 Players"},  
        {id:"background", label:"🟣 Backgrounds"},  
        {id:"obstacle", label:"🟥 Obstacles"},  
      ];  
  
      types.forEach(t => {  
        const title = document.createElement("div");  
        title.className = "collection-section-title";  
        title.textContent = t.label;  
        collectionBody.appendChild(title);  
  
        const wrap = document.createElement("div");  
        wrap.className = "collection-type-block";  
  
        let filtered = SKINS.filter(s => s.type === t.id && (rarity === 'all' ? true : s.rarity === rarity));  
  
        if (filtered.length === 0){  
          const empty = document.createElement("div");  
          empty.style.opacity = ".4";  
          empty.style.fontSize = "12px";  
          empty.textContent = "(none in this rarity)";  
          wrap.appendChild(empty);  
        } else {  
          filtered.forEach(skin => {  
            const card = buildSkinCard(skin, rarity);  
            wrap.appendChild(card);  
          });  
        }  
  
        collectionBody.appendChild(wrap);  
      });  
    }  
  
    // ===== Daily reward =====  
    function claimDaily(){  
      const now = Date.now();  
      const dayMs = 24 * 60 * 60 * 1000;  
      if (now - lastDaily >= dayMs){  
        const reward = 20 + Math.floor(Math.random()*90); // 20-109  
        coins += reward;  
        lastDaily = now;  
        localStorage.setItem("rg-lastDaily", lastDaily);  
        coinAmountEl.textContent = coins;  
        saveAll();  
        alert("Daily reward claimed: " + reward + " coins");  
        playBeep(1200,0.14,'sine',0.06);  
      } else {  
        const remaining = Math.ceil((dayMs - (now - lastDaily)) / (60*1000));  
        alert("Daily reward already claimed. Try again in " + remaining + " minutes.");  
        playBeep(220,0.07);  
      }  
    }  
  
    // ===== Pause/resume and keyboard controls =====  
    function togglePause(){  
      if (!running) return;  
      paused = !paused;  
      pauseBtn.textContent = paused ? '▶️' : '⏸';  
      playBeep(600,0.07);  
    }  
  
    document.addEventListener("keydown", (e) => {  
      if (e.code === "Space") { e.preventDefault(); jump(); }  
      if (e.key.toLowerCase() === "p") togglePause();  
      if (e.key.toLowerCase() === "g") openGacha();  
      if (e.key.toLowerCase() === "c") openCollection();  
    });  
  
    // touch and click for jump  
    canvas.addEventListener("touchstart", (ev) => {  
      ev.preventDefault();  
      if (!menuOpen && running) jump();  
      else if (!running && menuOpen && !paused) { /* ignore */ }  
    }, {passive:false});  
  
    canvas.addEventListener("click", () => {  
      if (!menuOpen && running) jump();  
    });  
  
    // ===== Gacha wheel button hook =====  
    document.getElementById("spinBtn").addEventListener("click", spinWheel);  
  
    // update coin ui live when changed externally  
    function refreshUI(){ coinAmountEl.textContent = coins; gachaCoins.textContent = "Your coins: " + coins; updatePityText(); bestEl.textContent = best; scoreEl.textContent = score; }  
    setInterval(refreshUI, 1000);  
  
    // initialize UI text  
    refreshUI();  
  
    // expose some functions to window for inline buttons  
    window.openGacha = openGacha;  
    window.closeGacha = closeGacha;  
    window.openCollection = openCollection;  
    window.closeCollection = closeCollection;  
    window.selectDifficulty = selectDifficulty;  
    window.claimDaily = claimDaily;  
    window.togglePause = togglePause;  
    window.toggleSound = toggleSound;  
  
    // Load initial owned defaults: give a couple of starting skins (friendly)  
    function ensureStarterSkins(){  
      let changed = false;  
      if (!ownedSkins.player.includes("Blue Block")) { ownedSkins.player.push("Blue Block"); changed = true; }  
      if (!ownedSkins.background.includes("Simple Background")) { ownedSkins.background.push("Simple Background"); changed = true; }  
      if (!ownedSkins.obstacle.includes("Grey Obstacle")) { ownedSkins.obstacle.push("Grey Obstacle"); changed = true; }  
      if (changed) saveAll();  
    }  
    ensureStarterSkins();  
  
    // show a friendly tooltip on first load (only once)  
    if (!localStorage.getItem("rg-seenTips")){  
      setTimeout(()=>{ alert("Tip: Press Space to jump. Use 🎰 to spin for new skins (30 coins). You get a guaranteed Legendary after 50 spins for a given type."); localStorage.setItem("rg-seenTips","1"); }, 600);  
    }  
  
    // ensure selection exists  
    if (!selectedSkins.player) selectedSkins.player = "default";  
    if (!selectedSkins.background) selectedSkins.background = "default";  
    if (!selectedSkins.obstacle) selectedSkins.obstacle = "default";  
    if (!pity.player) pity.player = 0;  
    if (!pity.background) pity.background = 0;  
    if (!pity.obstacle) pity.obstacle = 0;  
  
    // small visual redrawing for gacha wheel when loaded  
    drawWheel(0);  
  
    // Resume audio context on first user gesture (for browsers that block)  
    window.addEventListener('click', function resumeAudioOnGesture(){  
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();  
      window.removeEventListener('click', resumeAudioOnGesture);  
    });  
  
  </script>  
</body>  
</html>  
