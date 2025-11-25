const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json({ limit: "5mb" }));
app.use(bodyParser.urlencoded({ extended: true }));

// Fake lockers với _id
let lockers = [
  { _id: "1", name: "Locker 1", status: "closed" },
  { _id: "2", name: "Locker 2", status: "closed" },
  { _id: "3", name: "Locker 3", status: "closed" },
];

// Fake logs
let logs = [
  {
    _id: "1",
    lockerId: "1",
    action: "Locker 1 opened",
    time: new Date().toISOString(),
  },
  {
    _id: "2",
    lockerId: "2",
    action: "Locker 2 opened",
    time: new Date().toISOString(),
  },
];

// GET /api/lockers
app.get("/api/lockers", (req, res) => {
  res.json(lockers);
});

// GET /api/logs
app.get("/api/logs", (req, res) => {
  res.json(logs);
});

// POST /api/reset-lockers
app.post("/api/reset-lockers", (req, res) => {
  lockers = lockers.map((l) => ({ ...l, status: "closed" }));
  res.json({ success: true, lockers });
});

// POST /api/face
app.post("/api/face", (req, res) => {
  // Giả lập nhận diện thành công
  // Lấy lockerId từ body hoặc formData
  const lockerId =
    req.body.lockerId || (req.body.get && req.body.get("lockerId"));
  const locker = lockers.find((l) => l._id === lockerId);

  if (!locker) {
    return res.status(404).json({ message: "Locker not found" });
  }

  locker.status = "open";

  const log = {
    _id: (logs.length + 1).toString(),
    lockerId: locker._id,
    action: `${locker.name} opened via face recognition`,
    time: new Date().toISOString(),
  };
  logs.unshift(log); // thêm log mới lên đầu

  res.json({ locker, log });
});

// POST /api/lockers/:id/open
app.post("/api/lockers/:id/open", (req, res) => {
  const locker = lockers.find((l) => l._id === req.params.id);
  if (!locker) return res.status(404).json({ message: "Locker not found" });

  locker.status = "open";
  const log = {
    _id: (logs.length + 1).toString(),
    lockerId: locker._id,
    action: `${locker.name} opened manually`,
    time: new Date().toISOString(),
  };
  logs.unshift(log);

  res.json({ locker, log });
});

// POST /api/lockers/:id/close
app.post("/api/lockers/:id/close", (req, res) => {
  const locker = lockers.find((l) => l._id === req.params.id);
  if (!locker) return res.status(404).json({ message: "Locker not found" });

  locker.status = "closed";
  res.json({ locker });
});

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
