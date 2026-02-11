import { useEffect, useState } from "react";
import { apiFetch, authHeaders, clearToken, getToken } from "../lib/api";
import type { User } from "../lib/types";

function fmt(iso: string) {
  return new Date(iso).toLocaleString("fr-FR");
}

export default function Me() {
  const [me, setMe] = useState<User | null>(null);
  const [msg, setMsg] = useState("");

  async function loadMe() {
    setMsg("");
    try {
      const data = await apiFetch<User>("/me", { headers: { ...authHeaders() } });
      setMe(data);
    } catch (e: any) {
      setMe(null);
      setMsg("Non authentifié ou token invalide. Va dans Auth.");
    }
  }

  useEffect(() => {
    if (getToken()) loadMe();
  }, []);

  return (
    <>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>Session</h2>
        <div>
          Token:{" "}
          <span className={`badge ${getToken() ? "ok" : "ko"}`}>
            {getToken() ? "Présent" : "Absent"}
          </span>
        </div>
        <div className="row" style={{ marginTop: 12 }}>
          <div className="col"><button className="secondary" onClick={loadMe}>Recharger /me</button></div>
          <div className="col">
            <button
              className="secondary"
              onClick={() => {
                clearToken();
                setMe(null);
                setMsg("Déconnecté.");
              }}
            >
              Déconnexion
            </button>
          </div>
        </div>
        {msg && <div className="small" style={{ marginTop: 10, color: "#fca5a5" }}>{msg}</div>}
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0 }}>Profil</h2>
        {!me && <div className="small">Aucun profil chargé.</div>}
        {me && (
          <div className="grid" style={{ marginTop: 12 }}>
            <div className="tile"><b>Email</b><div className="small">{me.email}</div></div>
            <div className="tile"><b>Rôle</b><div className="small">{me.role}</div></div>
            <div className="tile"><b>ID</b><div className="small">{me.id}</div></div>
            <div className="tile"><b>Créé le</b><div className="small">{fmt(me.created_at)}</div></div>
          </div>
        )}
      </div>
    </>
  );
}
