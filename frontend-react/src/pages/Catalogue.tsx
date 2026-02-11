import { useEffect, useMemo, useState } from "react";
import { apiBase, apiFetch } from "../lib/api";
import type { Category } from "../lib/types";

function fmt(iso: string) {
  return new Date(iso).toLocaleString("fr-FR");
}

export default function Catalogue() {
  const [cats, setCats] = useState<Category[]>([]);
  const [q, setQ] = useState("");
  const [sort, setSort] = useState<"name" | "date">("name");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      setLoading(true);
      setErr(null);
      try {
        const data = await apiFetch<Category[]>("/categories");
        setCats(data);
      } catch {
        setErr("Impossible de charger les catégories (API indisponible ?)");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const filtered = useMemo(() => {
    const qq = q.trim().toLowerCase();
    let list = cats.filter((c) => c.name.toLowerCase().includes(qq));
    list = [...list].sort((a, b) => {
      if (sort === "name") return a.name.localeCompare(b.name);
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });
    return list;
  }, [cats, q, sort]);

  return (
    <>
      <div className="card">
        <div><b>API</b> : <span className="small">{apiBase}</span></div>
        <div className="small">
          Catalogue public : consultation des catégories sans authentification.
        </div>
      </div>

      <div className="card">
        <div className="row">
          <div className="col">
            <label>Recherche</label>
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ex: Montres" />
          </div>
          <div className="col">
            <label>Trier</label>
            <select value={sort} onChange={(e) => setSort(e.target.value as any)}>
              <option value="name">Nom A→Z</option>
              <option value="date">Plus récentes</option>
            </select>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0 }}>Catégories</h2>
        {loading && <div className="small">Chargement…</div>}
        {err && <div className="small" style={{ color: "#fca5a5" }}>{err}</div>}
        <div className="small">{filtered.length} catégorie(s)</div>

        <div className="grid" style={{ marginTop: 12 }}>
          {filtered.map((c) => (
            <div key={c.id} className="tile">
              <div style={{ fontWeight: 900, fontSize: 16 }}>{c.name}</div>
              <div className="small">Créée le {fmt(c.created_at)}</div>
              <div className="small">Public (catalogue)</div>
            </div>
          ))}
          {!loading && filtered.length === 0 && (
            <div className="small">Aucune catégorie. Connecte-toi en admin pour en créer.</div>
          )}
        </div>
      </div>
    </>
  );
}
