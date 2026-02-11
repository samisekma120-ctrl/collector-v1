import { useState } from "react";
import { apiFetch, authHeaders } from "../lib/api";
import type { Category } from "../lib/types";

export default function Admin() {
  const [name, setName] = useState("");
  const [msg, setMsg] = useState("");

  async function create() {
    setMsg("");
    try {
      const data = await apiFetch<Category>("/categories", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ name }),
      });
      setMsg(`✅ Catégorie créée: ${data.name}`);
      setName("");
    } catch (e: any) {
      if (e?.status === 403) setMsg("❌ 403 : admin requis");
      else if (e?.status === 409) setMsg("❌ 409 : catégorie déjà existante");
      else setMsg(`❌ Erreur: ${JSON.stringify(e.body ?? e)}`);
    }
  }

  return (
    <>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>Back-office – Catégories</h2>
        <div className="small">
          Conformité cahier des charges : création de catégories réservée admin.
        </div>

        <label>Nom de catégorie</label>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Ex: Montres" />
        <button onClick={create} disabled={!name.trim()}>Créer</button>

        {msg && <div className="small" style={{ marginTop: 10 }}>{msg}</div>}
      </div>
    </>
  );
}
