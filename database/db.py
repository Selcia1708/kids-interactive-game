import json
import hashlib
import streamlit as st
from datetime import datetime
from sqlalchemy import text          # ← ADD THIS IMPORT

def _conn():
    return st.connection("kids_db", type="sql")


# ── Schema ────────────────────────────────────────────────────────────────────
def init_db():
    conn = _conn()
    with conn.session as s:
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS profiles (
                id          INTEGER PRIMARY KEY,
                name        TEXT    NOT NULL,
                age         INTEGER,
                avatar      TEXT,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
                last_login  TEXT
            )
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS progress (
                id          INTEGER PRIMARY KEY,
                profile_id  INTEGER REFERENCES profiles(id),
                stars       INTEGER DEFAULT 0,
                xp          INTEGER DEFAULT 0,
                skill_json  TEXT    DEFAULT '{}',
                badges_json TEXT    DEFAULT '[]',
                updated_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY,
                profile_id  INTEGER REFERENCES profiles(id),
                world       TEXT,
                score       INTEGER,
                duration_s  INTEGER,
                played_at   TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS achievements (
                id          INTEGER PRIMARY KEY,
                profile_id  INTEGER REFERENCES profiles(id),
                badge_name  TEXT,
                earned_at   TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS parents (
                id          INTEGER PRIMARY KEY,
                email       TEXT    UNIQUE NOT NULL,
                pwd_hash    TEXT    NOT NULL,
                child_name  TEXT,
                child_age   INTEGER,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """))
        s.commit()


# ── Password hashing ──────────────────────────────────────────────────────────
def _hash(pwd: str) -> str:
    return hashlib.sha256(pwd.strip().encode()).hexdigest()


# ── Parent auth ───────────────────────────────────────────────────────────────
def register_parent(email: str, pwd: str, child_name: str, child_age: int) -> bool:
    conn = _conn()
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO parents (email, pwd_hash, child_name, child_age) VALUES (:e,:p,:cn,:ca)"),
                {"e": email.strip().lower(), "p": _hash(pwd),
                 "cn": child_name.strip(), "ca": child_age}
            )
            s.commit()
        return True
    except Exception:
        return False


def verify_parent(email: str, pwd: str):
    conn = _conn()
    df = conn.query(
        "SELECT * FROM parents WHERE email=:e AND pwd_hash=:p",
        params={"e": email.strip().lower(), "p": _hash(pwd)},
        ttl=0,
    )
    return df.iloc[0].to_dict() if not df.empty else None


def get_parent_by_email(email: str):
    conn = _conn()
    df = conn.query(
        "SELECT * FROM parents WHERE email=:e",
        params={"e": email.strip().lower()},
        ttl=0,
    )
    return df.iloc[0].to_dict() if not df.empty else None


# ── Profile CRUD ──────────────────────────────────────────────────────────────
def save_profile(name: str, age: int, avatar: str) -> int:
    now  = datetime.now().isoformat()
    conn = _conn()

    existing = conn.query(
        "SELECT id FROM profiles WHERE name=:n AND age=:a",
        params={"n": name, "a": age},
        ttl=0,
    )

    with conn.session as s:
        if not existing.empty:
            pid = int(existing.iloc[0]["id"])
            s.execute(
                text("UPDATE profiles SET last_login=:t, avatar=:av WHERE id=:id"),
                {"t": now, "av": avatar, "id": pid}
            )
        else:
            result = s.execute(
                text("INSERT INTO profiles (name, age, avatar, last_login) VALUES (:n,:a,:av,:t)"),
                {"n": name, "a": age, "av": avatar, "t": now}
            )
            pid = result.lastrowid
            s.execute(
                text("INSERT INTO progress (profile_id) VALUES (:pid)"),
                {"pid": pid}
            )
        s.commit()
    return pid


def load_profile(name: str, age: int):
    conn = _conn()
    df = conn.query(
        """SELECT p.id, p.name, p.age, p.avatar,
                  pr.stars, pr.xp, pr.skill_json, pr.badges_json
           FROM profiles p
           JOIN progress pr ON p.id = pr.profile_id
           WHERE p.name=:n AND p.age=:a""",
        params={"n": name, "a": age},
        ttl=0,
    )
    if df.empty:
        return None
    row = df.iloc[0]
    default_skills = {"phonics": 0, "math": 0, "logic": 0, "science": 0, "creativity": 0}
    raw_skills     = json.loads(row["skill_json"]   or "{}")
    merged         = {**default_skills, **raw_skills}
    return {
        "id":           int(row["id"]),
        "name":         row["name"],
        "age":          int(row["age"]),
        "avatar":       row["avatar"],
        "stars":        int(row["stars"]),
        "xp":           int(row["xp"]),
        "skill_scores": merged,
        "badges":       json.loads(row["badges_json"] or "[]"),
    }


def save_progress(profile_id: int, stars: int, xp: int,
                  skill_scores: dict, badges: list):
    now  = datetime.now().isoformat()
    conn = _conn()
    with conn.session as s:
        s.execute(
            text("""UPDATE progress
               SET stars=:s, xp=:x, skill_json=:sk, badges_json=:b, updated_at=:t
               WHERE profile_id=:pid"""),
            {"s": stars, "x": xp,
             "sk": json.dumps(skill_scores), "b": json.dumps(badges),
             "t": now, "pid": profile_id}
        )
        s.commit()


def log_session(profile_id: int, world: str, score: int, duration_s: int):
    conn = _conn()
    with conn.session as s:
        s.execute(
            text("INSERT INTO sessions (profile_id, world, score, duration_s) VALUES (:pid,:w,:sc,:d)"),
            {"pid": profile_id, "w": world, "sc": score, "d": duration_s}
        )
        s.commit()


def log_achievement(profile_id: int, badge_name: str):
    conn = _conn()
    existing = conn.query(
        "SELECT id FROM achievements WHERE profile_id=:pid AND badge_name=:b",
        params={"pid": profile_id, "b": badge_name},
        ttl=0,
    )
    if existing.empty:
        with conn.session as s:
            s.execute(
                text("INSERT INTO achievements (profile_id, badge_name) VALUES (:pid,:b)"),
                {"pid": profile_id, "b": badge_name}
            )
            s.commit()


def get_session_history(profile_id: int, limit: int = 10):
    conn = _conn()
    df = conn.query(
        "SELECT * FROM sessions WHERE profile_id=:pid ORDER BY played_at DESC LIMIT :lim",
        params={"pid": profile_id, "lim": limit},
        ttl=0,
    )
    return df.to_dict(orient="records")


def get_leaderboard(limit: int = 10):
    conn = _conn()
    df = conn.query(
        """SELECT p.name, p.avatar, pr.stars, pr.xp,
                  (SELECT COUNT(*) FROM achievements a WHERE a.profile_id=p.id) AS badge_count
           FROM profiles p
           JOIN progress pr ON p.id = pr.profile_id
           ORDER BY pr.xp DESC LIMIT :lim""",
        params={"lim": limit},
        ttl=0,
    )
    return df.to_dict(orient="records")


def get_all_profiles():
    conn = _conn()
    df = conn.query(
        """SELECT p.name, p.age, p.avatar, pr.stars, pr.xp
           FROM profiles p
           JOIN progress pr ON p.id = pr.profile_id
           ORDER BY p.last_login DESC""",
        ttl=0,
    )
    return df.to_dict(orient="records")


def get_child_full_stats(child_name: str, child_age: int):
    profile = load_profile(child_name, child_age)
    if not profile:
        return None
    sessions = get_session_history(profile["id"], limit=20)
    conn = _conn()
    df = conn.query(
        "SELECT badge_name, earned_at FROM achievements WHERE profile_id=:pid ORDER BY earned_at DESC",
        params={"pid": profile["id"]},
        ttl=0,
    )
    achievements = df.to_dict(orient="records")
    return {**profile, "sessions": sessions, "achievements": achievements}