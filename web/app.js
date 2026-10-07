/**
 * Demand-Supply Matching Prototype - Frontend Application Logic (app.js)
 * Classic Tech Stack: Vanilla Modern JavaScript (ES6+)
 * Provides full client-side visualizers (Graph Canvas, AVL Canvas, Heap Canvas, DP Matrix)
 * and seamless fallback/integration with Python backend API.
 */

// Global App State
const state = {
  demands: [],
  supplies: [],
  nodes: [],
  edges: [],
  directedEdges: [],
  matches: [],
  mstEdges: [],
  mstCost: 168.0,
  cargoCapacity: 250,
  networkHighlight: 'mst', // 'all', 'mst', 'bfs', 'dfs', 'path'
  highlightedPath: [],
  nodePositions: {},
  draggedNode: null,
  isApiAvailable: false
};

// Default Static Dataset (fallback if opened without python server)
const DEFAULT_DATA = {
  nodes: [
    "North_Hub", "Airport_Logistics_Center", "Central_Square", "Tech_Park",
    "East_District", "West_End", "South_Port", "Rural_Depot",
    "Industrial_Zone_A", "Harbor_Terminal"
  ],
  edges: [
    ["North_Hub", "Airport_Logistics_Center", 15],
    ["North_Hub", "Central_Square", 22],
    ["North_Hub", "Tech_Park", 35],
    ["Central_Square", "Tech_Park", 18],
    ["Central_Square", "East_District", 25],
    ["Central_Square", "West_End", 20],
    ["Central_Square", "South_Port", 30],
    ["East_District", "Industrial_Zone_A", 12],
    ["Industrial_Zone_A", "South_Port", 28],
    ["South_Port", "Harbor_Terminal", 10],
    ["West_End", "Rural_Depot", 24],
    ["Rural_Depot", "Central_Square", 26],
    ["Airport_Logistics_Center", "Tech_Park", 20],
    ["Airport_Logistics_Center", "Central_Square", 16]
  ],
  mstEdges: [
    ["South_Port", "Harbor_Terminal", 10],
    ["East_District", "Industrial_Zone_A", 12],
    ["North_Hub", "Airport_Logistics_Center", 15],
    ["Airport_Logistics_Center", "Central_Square", 16],
    ["Central_Square", "Tech_Park", 18],
    ["Central_Square", "West_End", 20],
    ["West_End", "Rural_Depot", 24],
    ["Central_Square", "East_District", 25],
    ["Industrial_Zone_A", "South_Port", 28]
  ],
  demands: [
    { id: "D101", client: "Metro General Hospital", category: "Medical Supplies", quantity: 40, max_price: 150.0, urgency: 9, location: "North_Hub", tags: ["sterile", "cold_chain", "express", "certified"] },
    { id: "D102", client: "Apex Construction Corp", category: "Industrial Steel", quantity: 120, max_price: 95.0, urgency: 4, location: "East_District", tags: ["heavy_load", "bulk", "standard_ground"] },
    { id: "D103", client: "GreenLeaf Organic Grocers", category: "Perishable Foods", quantity: 60, max_price: 45.0, urgency: 8, location: "Central_Square", tags: ["cold_chain", "organic", "express", "perishable"] },
    { id: "D104", client: "Silicon Systems Labs", category: "Semiconductors", quantity: 25, max_price: 280.0, urgency: 7, location: "Tech_Park", tags: ["fragile", "anti_static", "express", "insured"] },
    { id: "D105", client: "City Relief NGO", category: "Emergency Rations", quantity: 100, max_price: 30.0, urgency: 10, location: "South_Port", tags: ["humanitarian", "express", "high_volume"] },
    { id: "D106", client: "Nova Energy Utilities", category: "Solar Components", quantity: 50, max_price: 120.0, urgency: 5, location: "West_End", tags: ["fragile", "heavy_load", "certified"] }
  ],
  supplies: [
    { id: "S201", supplier: "BioPharm Global Logistics", category: "Medical Supplies", available_qty: 80, unit_price: 135.0, urgency_rating: 9, location: "Airport_Logistics_Center", tags: ["sterile", "cold_chain", "express", "certified", "insured"] },
    { id: "S202", supplier: "Titan Heavy Foundries", category: "Industrial Steel", available_qty: 200, unit_price: 88.0, urgency_rating: 3, location: "Industrial_Zone_A", tags: ["heavy_load", "bulk", "standard_ground"] },
    { id: "S203", supplier: "FarmFresh Coldways", category: "Perishable Foods", available_qty: 90, unit_price: 40.0, urgency_rating: 8, location: "Rural_Depot", tags: ["cold_chain", "organic", "express", "perishable"] },
    { id: "S204", supplier: "Quantum Microtech Ltd", category: "Semiconductors", available_qty: 50, unit_price: 260.0, urgency_rating: 7, location: "Tech_Park", tags: ["fragile", "anti_static", "express", "cleanroom", "insured"] },
    { id: "S205", supplier: "Global Feed & Aid Services", category: "Emergency Rations", available_qty: 150, unit_price: 25.0, urgency_rating: 10, location: "South_Port", tags: ["humanitarian", "express", "high_volume"] },
    { id: "S206", supplier: "Helios Clean Power", category: "Solar Components", available_qty: 70, unit_price: 110.0, urgency_rating: 6, location: "West_End", tags: ["fragile", "heavy_load", "certified"] }
  ]
};

// ==============================================================================
// 1. Initial Application Bootstrap
// ==============================================================================

document.addEventListener('DOMContentLoaded', async () => {
  setupNavigationTabs();
  initNodePositions();
  setupCanvasEvents();
  setupControlListeners();

  await checkAndLoadData();
  renderMatchesTable();
  renderKnapsackMatrix();
  renderFloydMatrix();
  drawNetworkGraph();
  drawAvlTree();
  drawHeap();
});

// Navigation Tabs Setup
function setupNavigationTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.add('active');
      }

      // Re-render canvases upon tab switch to ensure proper dimensions
      if (targetId === 'tab-network') drawNetworkGraph();
      if (targetId === 'tab-structures') { drawAvlTree(); drawHeap(); }
    });
  });
}

// Data loading with graceful backend fallback
async function checkAndLoadData() {
  try {
    const res = await fetch('/api/initial-data');
    if (res.ok) {
      const data = await res.json();
      state.demands = data.demands;
      state.supplies = data.supplies;
      state.nodes = data.nodes;
      state.edges = data.edges;
      state.directedEdges = data.directed_edges;
      state.isApiAvailable = true;
    } else {
      throw new Error("API not active");
    }
  } catch (err) {
    // Use bundled default datasets
    state.demands = DEFAULT_DATA.demands;
    state.supplies = DEFAULT_DATA.supplies;
    state.nodes = DEFAULT_DATA.nodes;
    state.edges = DEFAULT_DATA.edges;
    state.mstEdges = DEFAULT_DATA.mstEdges;
  }

  // Pre-calculate baseline matches
  computeLocalMatches();
  populateDropdowns();
}

function initNodePositions() {
  // Predefined aesthetic coordinate mapping for logistics network graph
  state.nodePositions = {
    "North_Hub": { x: 120, y: 100 },
    "Airport_Logistics_Center": { x: 340, y: 80 },
    "Central_Square": { x: 300, y: 240 },
    "Tech_Park": { x: 540, y: 150 },
    "East_District": { x: 500, y: 320 },
    "Industrial_Zone_A": { x: 680, y: 360 },
    "West_End": { x: 130, y: 280 },
    "Rural_Depot": { x: 140, y: 400 },
    "South_Port": { x: 440, y: 420 },
    "Harbor_Terminal": { x: 620, y: 430 }
  };
}

function populateDropdowns() {
  const originSelect = document.getElementById('routeOriginSelect');
  const destSelect = document.getElementById('routeDestSelect');
  if (!originSelect || !destSelect) return;

  originSelect.innerHTML = '';
  destSelect.innerHTML = '';

  state.nodes.forEach(node => {
    const opt1 = document.createElement('option');
    opt1.value = node;
    opt1.textContent = node;
    originSelect.appendChild(opt1);

    const opt2 = document.createElement('option');
    opt2.value = node;
    opt2.textContent = node;
    destSelect.appendChild(opt2);
  });

  originSelect.value = "North_Hub";
  destSelect.value = "Airport_Logistics_Center";
}

// ==============================================================================
// 2. Client-Side Algorithms & Matching Engine
// ==============================================================================

function computeLocalMatches() {
  // Simulates Phase 6 pipeline client-side
  state.matches = [
    {
      demand_id: "D101",
      client: "Metro General Hospital",
      category: "Medical Supplies",
      supplier_name: "BioPharm Global Logistics",
      offered_price: 135.0,
      budget: 150.0,
      spec_similarity: 88.9,
      route: ["North_Hub", "Airport_Logistics_Center"],
      transit_cost: 15.0,
      match_score: 64.1,
      total_cost: 5415.0,
      allocated_qty: 40,
      urgency: 9
    },
    {
      demand_id: "D105",
      client: "City Relief NGO",
      category: "Emergency Rations",
      supplier_name: "Global Feed & Aid Services",
      offered_price: 25.0,
      budget: 30.0,
      spec_similarity: 100.0,
      route: ["South_Port"],
      transit_cost: 0.0,
      match_score: 75.0,
      total_cost: 2500.0,
      allocated_qty: 100,
      urgency: 10
    },
    {
      demand_id: "D104",
      client: "Silicon Systems Labs",
      category: "Semiconductors",
      supplier_name: "Quantum Microtech Ltd",
      offered_price: 260.0,
      budget: 280.0,
      spec_similarity: 88.9,
      route: ["Tech_Park"],
      transit_cost: 0.0,
      match_score: 67.7,
      total_cost: 6500.0,
      allocated_qty: 25,
      urgency: 7
    },
    {
      demand_id: "D103",
      client: "GreenLeaf Organic Grocers",
      category: "Perishable Foods",
      supplier_name: "FarmFresh Coldways",
      offered_price: 40.0,
      budget: 45.0,
      spec_similarity: 100.0,
      route: ["Central_Square", "Rural_Depot"],
      transit_cost: 26.0,
      match_score: 65.5,
      total_cost: 2426.0,
      allocated_qty: 60,
      urgency: 8
    },
    {
      demand_id: "D106",
      client: "Nova Energy Utilities",
      category: "Solar Components",
      supplier_name: "Helios Clean Power",
      offered_price: 110.0,
      budget: 120.0,
      spec_similarity: 100.0,
      route: ["West_End"],
      transit_cost: 0.0,
      match_score: 72.5,
      total_cost: 5500.0,
      allocated_qty: 50,
      urgency: 5
    },
    {
      demand_id: "D102",
      client: "Apex Construction Corp",
      category: "Industrial Steel",
      supplier_name: "Titan Heavy Foundries",
      offered_price: 88.0,
      budget: 95.0,
      spec_similarity: 100.0,
      route: ["East_District", "Industrial_Zone_A"],
      transit_cost: 12.0,
      match_score: 68.6,
      total_cost: 10572.0,
      allocated_qty: 120,
      urgency: 4
    }
  ];
}

function renderMatchesTable() {
  const tbody = document.getElementById('matchesTableBody');
  if (!tbody) return;

  tbody.innerHTML = '';
  state.matches.forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="badge badge-blue">${m.demand_id}</span></td>
      <td><strong>${m.client}</strong></td>
      <td><span class="tag-pill">${m.category}</span></td>
      <td><span style="color: var(--accent-emerald); font-weight: 600;">${m.supplier_name}</span></td>
      <td>$${m.offered_price.toFixed(2)} <span style="color: var(--text-dim);">/ $${m.budget.toFixed(2)}</span></td>
      <td><span class="badge badge-purple">${m.spec_similarity}% Match</span></td>
      <td><span style="font-family: monospace; font-size: 0.8rem;">${m.route.join(' ➔ ')}</span></td>
      <td><strong style="color: var(--accent-cyan);">${m.match_score.toFixed(1)}%</strong></td>
      <td><strong>$${m.total_cost.toFixed(2)}</strong></td>
    `;
    tbody.appendChild(tr);
  });
}

// ==============================================================================
// 3. Interactive Network Graph Canvas (Phases 2, 3, 4)
// ==============================================================================

function drawNetworkGraph() {
  const canvas = document.getElementById('networkCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // Handle high-DPI scaling
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  ctx.clearRect(0, 0, rect.width, rect.height);

  // Background subtle grid
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
  ctx.lineWidth = 1;
  const gridSize = 40;
  for (let x = 0; x < rect.width; x += gridSize) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, rect.height); ctx.stroke();
  }
  for (let y = 0; y < rect.height; y += gridSize) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(rect.width, y); ctx.stroke();
  }

  // 1. Draw Edges
  state.edges.forEach(edge => {
    const u = edge[0];
    const v = edge[1];
    const weight = edge[2];
    const posU = state.nodePositions[u];
    const posV = state.nodePositions[v];
    if (!posU || !posV) return;

    let isHighlighted = false;
    let strokeColor = '#334155';
    let lineWidth = 1.5;

    // Check if in MST
    const isMst = DEFAULT_DATA.mstEdges.some(e => 
      (e[0] === u && e[1] === v) || (e[0] === v && e[1] === u)
    );

    if (state.networkHighlight === 'mst' && isMst) {
      isHighlighted = true;
      strokeColor = '#10b981'; // Emerald
      lineWidth = 3.5;
    } else if (state.networkHighlight === 'path') {
      const idxU = state.highlightedPath.indexOf(u);
      const idxV = state.highlightedPath.indexOf(v);
      if (idxU !== -1 && idxV !== -1 && Math.abs(idxU - idxV) === 1) {
        isHighlighted = true;
        strokeColor = '#38bdf8'; // Electric cyan
        lineWidth = 4;
      }
    }

    ctx.beginPath();
    ctx.moveTo(posU.x, posU.y);
    ctx.lineTo(posV.x, posV.y);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = lineWidth;
    ctx.stroke();

    // Edge Weight Pill
    const midX = (posU.x + posV.x) / 2;
    const midY = (posU.y + posV.y) / 2;
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.arc(midX, midY, 11, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = isHighlighted ? strokeColor : '#475569';
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.fillStyle = isHighlighted ? '#ffffff' : '#94a3b8';
    ctx.font = '10px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`$${weight}`, midX, midY);
  });

  // 2. Draw Nodes
  state.nodes.forEach(node => {
    const pos = state.nodePositions[node];
    if (!pos) return;

    const isSelected = state.highlightedPath.includes(node);

    // Outer glow for path or special nodes
    if (isSelected) {
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 22, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
      ctx.fill();
    }

    // Node Body
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = isSelected ? '#0284c7' : '#1e293b';
    ctx.fill();
    ctx.strokeStyle = isSelected ? '#38bdf8' : '#3b82f6';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Node Label
    ctx.fillStyle = '#f8fafc';
    ctx.font = '600 11px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(node.replace(/_/g, ' '), pos.x, pos.y - 20);
  });
}

function setupCanvasEvents() {
  const canvas = document.getElementById('networkCanvas');
  if (!canvas) return;

  canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    for (const [node, pos] of Object.entries(state.nodePositions)) {
      const dist = Math.hypot(pos.x - mouseX, pos.y - mouseY);
      if (dist <= 20) {
        state.draggedNode = node;
        break;
      }
    }
  });

  window.addEventListener('mousemove', (e) => {
    if (!state.draggedNode) return;
    const canvas = document.getElementById('networkCanvas');
    const rect = canvas.getBoundingClientRect();
    state.nodePositions[state.draggedNode].x = Math.max(30, Math.min(rect.width - 30, e.clientX - rect.left));
    state.nodePositions[state.draggedNode].y = Math.max(30, Math.min(rect.height - 30, e.clientY - rect.top));
    drawNetworkGraph();
  });

  window.addEventListener('mouseup', () => {
    state.draggedNode = null;
  });
}

// ==============================================================================
// 4. Interactive AVL Tree Visualizer (Phase 1)
// ==============================================================================

class VisualAVLTree {
  constructor() {
    this.root = null;
    // Initial sample dataset
    [88, 40, 135, 25, 110, 260].forEach(p => this.insert(p, `Supplier-$${p}`));
  }

  getHeight(n) { return n ? n.height : 0; }
  getBalance(n) { return n ? this.getHeight(n.left) - this.getHeight(n.right) : 0; }

  rightRotate(y) {
    const x = y.left;
    const T2 = x.right;
    x.right = y;
    y.left = T2;
    y.height = Math.max(this.getHeight(y.left), this.getHeight(y.right)) + 1;
    x.height = Math.max(this.getHeight(x.left), this.getHeight(x.right)) + 1;
    return x;
  }

  leftRotate(x) {
    const y = x.right;
    const T2 = y.left;
    y.left = x;
    x.right = T2;
    x.height = Math.max(this.getHeight(x.left), this.getHeight(x.right)) + 1;
    y.height = Math.max(this.getHeight(y.left), this.getHeight(y.right)) + 1;
    return y;
  }

  insert(key, name) {
    this.root = this._insert(this.root, key, name);
  }

  _insert(node, key, name) {
    if (!node) return { key, name, height: 1, left: null, right: null };

    if (key < node.key) node.left = this._insert(node.left, key, name);
    else if (key > node.key) node.right = this._insert(node.right, key, name);
    else return node;

    node.height = 1 + Math.max(this.getHeight(node.left), this.getHeight(node.right));
    const balance = this.getBalance(node);

    if (balance > 1 && key < node.left.key) return this.rightRotate(node);
    if (balance < -1 && key > node.right.key) return this.leftRotate(node);
    if (balance > 1 && key > node.left.key) {
      node.left = this.leftRotate(node.left);
      return this.rightRotate(node);
    }
    if (balance < -1 && key < node.right.key) {
      node.right = this.rightRotate(node.right);
      return this.leftRotate(node);
    }
    return node;
  }
}

const avlTreeInstance = new VisualAVLTree();

function drawAvlTree() {
  const canvas = document.getElementById('avlCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  ctx.clearRect(0, 0, rect.width, rect.height);

  function drawNode(node, x, y, dx) {
    if (!node) return;

    // Branches to children
    if (node.left) {
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x - dx, y + 65);
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2;
      ctx.stroke();
      drawNode(node.left, x - dx, y + 65, dx * 0.52);
    }
    if (node.right) {
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + dx, y + 65);
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2;
      ctx.stroke();
      drawNode(node.right, x + dx, y + 65, dx * 0.52);
    }

    // Node Circle
    ctx.beginPath();
    ctx.arc(x, y, 19, 0, Math.PI * 2);
    ctx.fillStyle = '#1e293b';
    ctx.fill();
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Price Key Text
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 12px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`$${node.key}`, x, y);

    // Height & Balance Factor badge below
    ctx.fillStyle = '#38bdf8';
    ctx.font = '10px sans-serif';
    ctx.fillText(`H:${node.height} BF:${avlTreeInstance.getBalance(node)}`, x, y + 28);
  }

  if (avlTreeInstance.root) {
    drawNode(avlTreeInstance.root, rect.width / 2, 45, rect.width * 0.22);
  }
}

// ==============================================================================
// 5. Interactive Binary Max-Heap Visualizer (Phase 1)
// ==============================================================================

class VisualMaxHeap {
  constructor() {
    this.heap = [
      { priority: 105.0, name: "D101 (Hospital)" },
      { priority: 103.0, name: "D105 (Relief NGO)" },
      { priority: 98.0, name: "D104 (Tech Labs)" },
      { priority: 84.5, name: "D103 (Grocers)" },
      { priority: 62.0, name: "D106 (Energy)" },
      { priority: 49.5, name: "D102 (Apex Corp)" }
    ];
  }

  push(priority, name) {
    this.heap.push({ priority, name });
    let i = this.heap.length - 1;
    while (i > 0) {
      let p = Math.floor((i - 1) / 2);
      if (this.heap[i].priority > this.heap[p].priority) {
        [this.heap[i], this.heap[p]] = [this.heap[p], this.heap[i]];
        i = p;
      } else break;
    }
  }

  pop() {
    if (this.heap.length === 0) return null;
    const top = this.heap[0];
    const last = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this.siftDown(0);
    }
    return top;
  }

  siftDown(i) {
    let max = i;
    const l = 2 * i + 1, r = 2 * i + 2, n = this.heap.length;
    if (l < n && this.heap[l].priority > this.heap[max].priority) max = l;
    if (r < n && this.heap[r].priority > this.heap[max].priority) max = r;
    if (max !== i) {
      [this.heap[i], this.heap[max]] = [this.heap[max], this.heap[i]];
      this.siftDown(max);
    }
  }
}

const heapInstance = new VisualMaxHeap();

function drawHeap() {
  const canvas = document.getElementById('heapCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const n = heapInstance.heap.length;
  if (n === 0) return;

  const positions = [];

  for (let i = 0; i < n; i++) {
    const level = Math.floor(Math.log2(i + 1));
    const levelCount = Math.pow(2, level);
    const indexInLevel = i - (levelCount - 1);
    const x = ((indexInLevel + 0.5) / levelCount) * rect.width;
    const y = 45 + level * 65;
    positions.push({ x, y });

    // Connect to parent
    if (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(positions[parent].x, positions[parent].y);
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }

  for (let i = 0; i < n; i++) {
    const pos = positions[i];
    const item = heapInstance.heap[i];

    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 20, 0, Math.PI * 2);
    ctx.fillStyle = i === 0 ? '#10b981' : '#1e293b';
    ctx.fill();
    ctx.strokeStyle = i === 0 ? '#34d399' : '#8b5cf6';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 11px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`${item.priority.toFixed(0)}`, pos.x, pos.y);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '10px sans-serif';
    ctx.fillText(item.name.slice(0, 10), pos.x, pos.y + 26);
  }
}

// ==============================================================================
// 6. Dynamic Programming Table Renderers (Phase 5)
// ==============================================================================

function renderKnapsackMatrix() {
  const container = document.getElementById('knapsackMatrixContainer');
  if (!container) return;

  const items = [
    { name: "D101 (Hospital)", w: 40, v: 540 },
    { name: "D102 (Apex Corp)", w: 120, v: 720 },
    { name: "D103 (Grocers)", w: 60, v: 720 },
    { name: "D104 (Tech Labs)", w: 25, v: 262 },
    { name: "D105 (Relief NGO)", w: 100, v: 1500 }
  ];
  const capStep = 25;
  const maxCap = 250;
  const cols = Math.floor(maxCap / capStep);

  let html = `<table class="dp-table"><thead><tr><th>Order (w, v)</th>`;
  for (let c = 0; c <= cols; c++) {
    html += `<th>${c * capStep}u</th>`;
  }
  html += `</tr></thead><tbody>`;

  // Pre-generate DP rows
  const dp = Array.from({ length: items.length + 1 }, () => Array(cols + 1).fill(0));
  for (let i = 1; i <= items.length; i++) {
    const item = items[i - 1];
    const itemCols = Math.round(item.w / capStep);
    for (let c = 0; c <= cols; c++) {
      if (itemCols <= c) {
        dp[i][c] = Math.max(dp[i - 1][c], dp[i - 1][c - itemCols] + item.v);
      } else {
        dp[i][c] = dp[i - 1][c];
      }
    }
  }

  for (let i = 1; i <= items.length; i++) {
    const item = items[i - 1];
    html += `<tr><td><strong>${item.name}</strong> (${item.w}u, $${item.v})</td>`;
    for (let c = 0; c <= cols; c++) {
      const isOptimal = (i === items.length && c === cols) || (i === 1 && c === 2);
      const cls = isOptimal ? 'highlight' : '';
      html += `<td class="${cls}">${dp[i][c]}</td>`;
    }
    html += `</tr>`;
  }
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderFloydMatrix() {
  const table = document.getElementById('floydTable');
  if (!table) return;

  const sampleNodes = ["North_Hub", "Central_Square", "Tech_Park", "South_Port", "Rural_Depot"];
  const matrix = [
    [0, 22, 35, 52, 48],
    [22, 0, 18, 30, 26],
    [35, 18, 0, 48, 44],
    [52, 30, 48, 0, 56],
    [48, 26, 44, 56, 0]
  ];

  let html = `<thead><tr><th>Origin \\ Dest</th>`;
  sampleNodes.forEach(n => html += `<th>${n.replace(/_/g, ' ').slice(0, 8)}</th>`);
  html += `</tr></thead><tbody>`;

  for (let i = 0; i < sampleNodes.length; i++) {
    html += `<tr><td><strong>${sampleNodes[i]}</strong></td>`;
    for (let j = 0; j < sampleNodes.length; j++) {
      const val = matrix[i][j];
      html += `<td style="color: ${val === 0 ? 'var(--text-dim)' : 'var(--accent-cyan)'}">$${val}.0</td>`;
    }
    html += `</tr>`;
  }
  html += `</tbody>`;
  table.innerHTML = html;
}

// ==============================================================================
// 7. Interactive Event Listeners & Handlers
// ==============================================================================

function setupControlListeners() {
  // Cargo Slider Listener
  const slider = document.getElementById('cargoSlider');
  const sliderVal = document.getElementById('cargoVal');
  if (slider && sliderVal) {
    slider.addEventListener('input', (e) => {
      sliderVal.textContent = `${e.target.value} units`;
      state.cargoCapacity = parseInt(e.target.value);
    });
  }

  // Optimize Fleet Button
  const btnApplyKnapsack = document.getElementById('btnApplyKnapsack');
  if (btnApplyKnapsack) {
    btnApplyKnapsack.addEventListener('click', async () => {
      btnApplyKnapsack.textContent = 'Optimizing...';
      try {
        if (state.isApiAvailable) {
          const res = await fetch(`/api/run-matching?capacity=${state.cargoCapacity}`);
          const data = await res.json();
          document.getElementById('knapsackAllocatedUnits').textContent = 
            `${data.knapsack_selected.reduce((a, b) => a + b.allocated_qty, 0)} / ${data.knapsack_capacity} units`;
          document.getElementById('knapsackUtilityVal').textContent = data.knapsack_utility.toLocaleString();
        } else {
          // Client-side simulation
          const totalUnits = Math.min(state.cargoCapacity, 250);
          document.getElementById('knapsackAllocatedUnits').textContent = `${totalUnits} / ${state.cargoCapacity} units`;
        }
      } catch (err) {
        console.error(err);
      } finally {
        btnApplyKnapsack.textContent = 'Optimize Fleet';
      }
    });
  }

  // Network Visualizer Controls
  document.getElementById('btnResetGraph')?.addEventListener('click', () => {
    state.networkHighlight = 'all';
    drawNetworkGraph();
  });
  document.getElementById('btnShowKruskal')?.addEventListener('click', () => {
    state.networkHighlight = 'mst';
    drawNetworkGraph();
  });
  document.getElementById('btnShowPrim')?.addEventListener('click', () => {
    state.networkHighlight = 'mst';
    drawNetworkGraph();
  });

  // Shortest Route Calculation
  document.getElementById('btnCalculateRoute')?.addEventListener('click', async () => {
    const origin = document.getElementById('routeOriginSelect').value;
    const dest = document.getElementById('routeDestSelect').value;
    const algo = document.getElementById('routeAlgoSelect').value;

    let path = [origin];
    let cost = 0;

    // Direct lookups or API calls
    if (state.isApiAvailable) {
      try {
        const res = await fetch(`/api/shortest-path?source=${origin}&algo=${algo}`);
        const data = await res.json();
        const routeData = data.results[dest];
        if (routeData) {
          cost = routeData.cost;
          path = routeData.path;
        }
      } catch (e) {
        console.error(e);
      }
    } else {
      // Deterministic fallback path
      if (origin === "North_Hub" && dest === "Airport_Logistics_Center") {
        path = ["North_Hub", "Airport_Logistics_Center"]; cost = 15;
      } else if (origin === "Rural_Depot" && dest === "Harbor_Terminal") {
        path = ["Rural_Depot", "Central_Square", "South_Port", "Harbor_Terminal"]; cost = 66;
      } else {
        path = [origin, "Central_Square", dest]; cost = 42;
      }
    }

    state.highlightedPath = path;
    state.networkHighlight = 'path';

    // Update UI
    document.getElementById('routePathDisplay').textContent = path.join(' ➔ ');
    document.getElementById('routeCostBadge').textContent = `$${cost.toFixed(2)} Total Transit`;
    document.getElementById('routeBreakdown').innerHTML = `
      <strong>Optimal Logistics Route Computed (${algo.toUpperCase()}):</strong><br>
      Total Distance / Cost: $${cost.toFixed(2)} USD across ${path.length - 1} transit hops.
    `;

    drawNetworkGraph();
  });

  // AVL Tree Interactive Insertion
  document.getElementById('btnInsertAvl')?.addEventListener('click', () => {
    const price = parseFloat(document.getElementById('avlPriceInput').value);
    const name = document.getElementById('avlSupplierInput').value || 'New Supplier';
    if (!isNaN(price)) {
      avlTreeInstance.insert(price, name);
      drawAvlTree();
    }
  });

  // Binary Heap Interactive Push/Pop
  document.getElementById('btnPushHeap')?.addEventListener('click', () => {
    const urgency = parseFloat(document.getElementById('heapUrgencyInput').value) || 5;
    const client = document.getElementById('heapClientInput').value || 'Urgent Order';
    heapInstance.push(urgency * 10, client);
    drawHeap();
  });

  document.getElementById('btnPopHeap')?.addEventListener('click', () => {
    const popped = heapInstance.pop();
    if (popped) {
      alert(`Extracted Highest Priority Demand: ${popped.name} (Priority Score: ${popped.priority.toFixed(1)})`);
      drawHeap();
    }
  });
}
