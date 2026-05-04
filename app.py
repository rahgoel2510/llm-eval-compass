"""LLM Eval Compass — Model Evaluation Dashboard.

Run with: streamlit run app.py
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import yaml

from connectors.mock_connector import DEMO_MODELS, MockConnector

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config"


# ── Helpers ──────────────────────────────────────────────────────────────────

@st.cache_data
def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_models() -> dict:
    real = load_yaml(str(CONFIG / "models.yaml")).get("models", {})
    return {**DEMO_MODELS, **real}


def load_profiles() -> dict:
    return load_yaml(str(CONFIG / "eval_weights.yaml")).get("profiles", {})


def load_thresholds() -> dict:
    return load_yaml(str(CONFIG / "thresholds.yaml"))


def find_test_sets() -> list[Path]:
    return sorted((ROOT / "benchmarks").rglob("*.json"))


def is_demo(model_key: str) -> bool:
    return model_key.startswith("demo-")


# ── Session state ────────────────────────────────────────────────────────────

if "eval_results" not in st.session_state:
    st.session_state.eval_results = {}

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="LLM Eval Compass", page_icon="🧭", layout="wide")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "🚀 Run Evaluation",
        "📊 Results",
        "⚖️ Compare Models",
        "💰 Cost Projector",
        "🔍 PII Scanner",
    ],
)


# ═════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════

if page == "🏠 Overview":
    st.title("🧭 LLM Eval Compass")
    st.markdown(
        "A production-grade framework for evaluating, comparing, and selecting LLMs. "
        "Connect your model → pick a test set → run evaluation → compare results."
    )

    st.info("🎭 **Try it now!** Demo models require no API key. Go to **🚀 Run Evaluation** and pick any 🎭 Demo model.")

    models = load_models()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Models Available", len(models))
    c2.metric("Use-Case Profiles", len(load_profiles()))
    c3.metric("Test Sets", len(find_test_sets()))
    c4.metric("Evaluations Run", len(st.session_state.eval_results))

    st.subheader("Model Registry")
    rows = []
    for mid, m in models.items():
        rows.append({
            "Model": m.get("display_name", mid),
            "Provider": m.get("provider", ""),
            "Context": f"{m.get('context_window', 0):,}",
            "Input $/1K": f"${m.get('input_cost_per_1k_tokens', 0)}",
            "Output $/1K": f"${m.get('output_cost_per_1k_tokens', 0)}",
            "Type": m.get("endpoint_type", ""),
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("How It Works")
    st.markdown("""
1. **🚀 Run Evaluation** — Pick a model (or a 🎭 Demo model), choose a test set, and run
2. **📊 Results** — View detailed scores, latency, cost, and per-case outputs
3. **⚖️ Compare Models** — Run 2+ models and compare side-by-side
4. **💰 Cost Projector** — Project costs at your expected query volume
5. **🔍 PII Scanner** — Test PII detection on any text
    """)


# ═════════════════════════════════════════════════════════════════════════════
# 2. RUN EVALUATION
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🚀 Run Evaluation":
    st.title("🚀 Run Model Evaluation")

    models = load_models()

    # Split demo and real models
    demo_keys = [k for k in models if is_demo(k)]
    real_keys = [k for k in models if not is_demo(k)]

    st.subheader("1. Select Model")

    model_tab_demo, model_tab_real = st.tabs(["🎭 Demo Models (no API key)", "🔑 Real Models (API key required)"])

    with model_tab_demo:
        demo_display = {models[k]["display_name"]: k for k in demo_keys}
        selected_demo = st.selectbox("Demo Model", list(demo_display.keys()), key="demo_sel")
        model_key = demo_display[selected_demo]
        st.success("✅ No API key needed — runs with simulated responses.")

    with model_tab_real:
        real_display = {f"{models[k].get('display_name', k)} ({models[k].get('provider', '')})" : k for k in real_keys}
        selected_real = st.selectbox("Model", list(real_display.keys()), key="real_sel")
        real_model_key = real_display[selected_real]

        real_cfg = models[real_model_key]
        provider = real_cfg["provider"]
        st.caption(f"Provider: **{provider}** · Context: {real_cfg.get('context_window', 0):,} tokens")

        if provider == "AWS Bedrock":
            c1, c2, c3 = st.columns(3)
            aws_key = c1.text_input("AWS Access Key ID", type="password")
            aws_secret = c2.text_input("AWS Secret Access Key", type="password")
            aws_region = c3.text_input("Region", value="us-east-1")
            api_key = None
            extra_kwargs = {"aws_access_key_id": aws_key, "aws_secret_access_key": aws_secret, "region": aws_region}
            has_real_creds = bool(aws_key and aws_secret)
        else:
            api_key = st.text_input(f"API Key ({provider})", type="password")
            extra_kwargs = {}
            has_real_creds = bool(api_key)

    # Determine which model to use based on active tab
    use_demo = True  # default to demo
    use_real = st.checkbox("Use real model instead of demo", value=False)
    if use_real:
        use_demo = False
        model_key = real_model_key

    model_cfg = models[model_key]

    st.caption(f"**Selected:** {model_cfg.get('display_name', model_key)} · "
               f"Cost: ${model_cfg.get('input_cost_per_1k_tokens', 0)}/1K in, "
               f"${model_cfg.get('output_cost_per_1k_tokens', 0)}/1K out")

    # Test set
    st.subheader("2. Select Test Set")
    test_sets = find_test_sets()
    test_set_labels = {str(p.relative_to(ROOT)): p for p in test_sets}

    uploaded = st.file_uploader("Or upload your own (JSON array)", type=["json"])
    if uploaded:
        up_path = ROOT / "benchmarks" / "uploaded_test_set.json"
        up_path.write_bytes(uploaded.read())
        test_set_labels[f"📎 {uploaded.name}"] = up_path

    selected_test = st.selectbox("Test Set", list(test_set_labels.keys()))
    test_path = test_set_labels[selected_test]

    with st.expander("Preview test set"):
        with open(test_path) as f:
            cases = json.load(f)
        st.write(f"**{len(cases)} test cases**")
        st.json(cases[:3])

    # Run button
    st.subheader("3. Run")
    can_run = use_demo or (use_real and has_real_creds)

    if st.button("▶ Run Evaluation", type="primary", disabled=not can_run):
        try:
            from engine import EvaluationEngine

            with st.spinner("Connecting..."):
                if use_demo:
                    conn = MockConnector(model_id=model_key)
                else:
                    from connectors import create_connector
                    conn = create_connector(model_key, api_key=api_key, **extra_kwargs)

            progress = st.progress(0, text="Starting...")
            status = st.empty()

            def on_progress(cur: int, total: int, tc_id: str):
                if total > 0:
                    progress.progress(cur / total, text=f"Running {tc_id} ({cur}/{total})")
                    status.caption(f"Test case: {tc_id}")

            engine = EvaluationEngine(conn)
            result = engine.run(str(test_path), progress_callback=on_progress)
            progress.progress(1.0, text="✅ Complete!")

            # Store
            rd = result.to_dict()
            rd["_case_details"] = [
                {"id": c.test_case_id, "input": c.input[:200], "expected": c.expected[:200],
                 "output": c.output[:200], "latency_ms": round(c.latency_ms, 1)}
                for c in result.test_case_results
            ]
            st.session_state.eval_results[model_key] = rd

            st.success(f"✅ **{model_cfg.get('display_name', model_key)}** — "
                       f"{len(result.test_case_results)} cases, {len(result.errors)} errors")

            c1, c2, c3 = st.columns(3)
            acc = result.scores.get("task_accuracy", {})
            c1.metric("Fuzzy Match", f"{acc.get('fuzzy_match', 0):.1%}")
            c2.metric("Avg Latency", f"{result.latency.get('mean_ms', 0):,.0f} ms")
            c3.metric("Total Cost", f"${result.cost.get('total_cost_usd', 0):.4f}")

            st.balloons()

        except Exception as e:
            st.error(f"Failed: {e}")

    if not can_run:
        st.warning("Enter API credentials above, or switch to a Demo model.")

    # Quick-run all demos
    st.divider()
    st.subheader("⚡ Quick: Run All Demo Models")
    st.caption("Evaluate all 4 demo models on the selected test set in one click.")
    if st.button("▶ Run All Demos", type="secondary"):
        from engine import EvaluationEngine

        overall_progress = st.progress(0, text="Starting batch...")
        for idx, (dk, dm) in enumerate(DEMO_MODELS.items()):
            overall_progress.progress((idx) / len(DEMO_MODELS), text=f"Evaluating {dm['display_name']}...")
            conn = MockConnector(model_id=dk)
            engine = EvaluationEngine(conn)
            result = engine.run(str(test_path))
            rd = result.to_dict()
            rd["_case_details"] = [
                {"id": c.test_case_id, "input": c.input[:200], "expected": c.expected[:200],
                 "output": c.output[:200], "latency_ms": round(c.latency_ms, 1)}
                for c in result.test_case_results
            ]
            st.session_state.eval_results[dk] = rd

        overall_progress.progress(1.0, text="✅ All demos complete!")
        st.success(f"Evaluated all {len(DEMO_MODELS)} demo models. Go to **📊 Results** or **⚖️ Compare Models**.")
        st.balloons()


# ═════════════════════════════════════════════════════════════════════════════
# 3. RESULTS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📊 Results":
    st.title("📊 Evaluation Results")

    if not st.session_state.eval_results:
        st.info("No evaluations yet. Go to **🚀 Run Evaluation** — try the demo models, no API key needed!")
    else:
        models_data = load_models()
        result_keys = list(st.session_state.eval_results.keys())
        selected = st.selectbox(
            "Select evaluation",
            result_keys,
            format_func=lambda k: models_data.get(k, {}).get("display_name", k),
        )
        r = st.session_state.eval_results[selected]

        st.subheader(models_data.get(selected, {}).get("display_name", selected))
        st.caption(f"Provider: {r['provider']} · Test set: {r['test_set']} · "
                   f"Run: {r['timestamp']} · Cases: {r['num_test_cases']} · Errors: {r['num_errors']}")

        # Scores
        c1, c2, c3, c4 = st.columns(4)
        acc = r["scores"].get("task_accuracy", {})
        c1.metric("Exact Match", f"{acc.get('exact_match', 0):.1%}")
        c2.metric("Fuzzy Match", f"{acc.get('fuzzy_match', 0):.1%}")
        pii = r["scores"].get("pii_leakage", {})
        c3.metric("PII Leakage", f"{pii.get('pii_leakage_rate', 0):.1%}")
        c4.metric("Total Cost", f"${r['cost'].get('total_cost_usd', 0):.4f}")

        # Latency
        st.subheader("Latency")
        lat = r.get("latency", {})
        cols = st.columns(len(lat))
        for i, (k, v) in enumerate(lat.items()):
            cols[i].metric(k.replace("_", " ").replace("ms", "").strip().title() + " (ms)", f"{v:,.0f}")

        # Cost
        st.subheader("Cost Breakdown")
        cost = r.get("cost", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Input Tokens", f"{cost.get('total_input_tokens', 0):,}")
        c2.metric("Output Tokens", f"{cost.get('total_output_tokens', 0):,}")
        c3.metric("Total Cost", f"${cost.get('total_cost_usd', 0):.6f}")
        c4.metric("Avg Cost/Query", f"${cost.get('avg_cost_per_query_usd', 0):.6f}")

        # Per-case
        st.subheader("Per-Case Details")
        details = r.get("_case_details", [])
        if details:
            st.dataframe(details, use_container_width=True, hide_index=True)

        if r["errors"]:
            st.subheader("Errors")
            for err in r["errors"]:
                st.error(err)

        # Export
        st.divider()
        export = {k: v for k, v in r.items() if k != "_case_details"}
        st.download_button("📥 Download Results (JSON)", json.dumps(export, indent=2), f"{selected}_results.json", "application/json")


# ═════════════════════════════════════════════════════════════════════════════
# 4. COMPARE MODELS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "⚖️ Compare Models":
    st.title("⚖️ Model Comparison")

    if len(st.session_state.eval_results) < 2:
        st.info(
            f"Need at least 2 evaluated models. You have **{len(st.session_state.eval_results)}**. "
            f"Go to **🚀 Run Evaluation** and click **Run All Demos** to quickly get comparison data."
        )
    else:
        models_data = load_models()
        result_keys = list(st.session_state.eval_results.keys())
        selected = st.multiselect(
            "Models to compare",
            result_keys,
            default=result_keys,
            format_func=lambda k: models_data.get(k, {}).get("display_name", k),
        )

        if len(selected) >= 2:
            rows = []
            for key in selected:
                r = st.session_state.eval_results[key]
                acc = r["scores"].get("task_accuracy", {})
                pii = r["scores"].get("pii_leakage", {})
                lat = r.get("latency", {})
                cost = r.get("cost", {})
                rows.append({
                    "Model": models_data.get(key, {}).get("display_name", key),
                    "Fuzzy Match": f"{acc.get('fuzzy_match', 0):.1%}",
                    "Exact Match": f"{acc.get('exact_match', 0):.1%}",
                    "PII Leakage": f"{pii.get('pii_leakage_rate', 0):.1%}",
                    "Avg Latency": f"{lat.get('mean_ms', 0):,.0f} ms",
                    "P95 Latency": f"{lat.get('p95_ms', 0):,.0f} ms",
                    "Cost/Query": f"${cost.get('avg_cost_per_query_usd', 0):.6f}",
                    "Total Cost": f"${cost.get('total_cost_usd', 0):.4f}",
                })

            st.subheader("Head-to-Head")
            st.dataframe(rows, use_container_width=True, hide_index=True)

            st.subheader("Charts")
            chart_metrics = {
                "Quality (Fuzzy Match)": lambda r: r["scores"].get("task_accuracy", {}).get("fuzzy_match", 0),
                "Avg Latency (ms)": lambda r: r.get("latency", {}).get("mean_ms", 0),
                "Cost per Query ($)": lambda r: r.get("cost", {}).get("avg_cost_per_query_usd", 0),
                "PII Leakage Rate": lambda r: r["scores"].get("pii_leakage", {}).get("pii_leakage_rate", 0),
            }

            cols = st.columns(2)
            for i, (name, fn) in enumerate(chart_metrics.items()):
                with cols[i % 2]:
                    data = {
                        models_data.get(k, {}).get("display_name", k): fn(st.session_state.eval_results[k])
                        for k in selected
                    }
                    st.markdown(f"**{name}**")
                    st.bar_chart(data)

            # Winner
            best = max(selected, key=lambda k: st.session_state.eval_results[k]["scores"].get("task_accuracy", {}).get("fuzzy_match", 0))
            best_name = models_data.get(best, {}).get("display_name", best)
            best_score = st.session_state.eval_results[best]["scores"].get("task_accuracy", {}).get("fuzzy_match", 0)
            st.success(f"🏆 **{best_name}** wins with {best_score:.1%} fuzzy match score.")


# ═════════════════════════════════════════════════════════════════════════════
# 5. COST PROJECTOR
# ═════════════════════════════════════════════════════════════════════════════

elif page == "💰 Cost Projector":
    st.title("💰 Cost Projector")
    models = load_models()
    model_names = {m.get("display_name", k): k for k, m in models.items()}

    selected = st.multiselect("Models", list(model_names.keys()), default=[
        v.get("display_name", k) for k, v in list(models.items())[:4]
    ])

    c1, c2, c3 = st.columns(3)
    qpd = c1.number_input("Queries / day", 100, 10_000_000, 10_000, step=1000)
    avg_in = c2.number_input("Avg input tokens", 10, 100_000, 500, step=50)
    avg_out = c3.number_input("Avg output tokens", 10, 100_000, 200, step=50)

    if selected:
        rows = []
        for dn in selected:
            mid = model_names[dn]
            m = models[mid]
            cpq = (avg_in * m.get("input_cost_per_1k_tokens", 0) + avg_out * m.get("output_cost_per_1k_tokens", 0)) / 1000
            daily = cpq * qpd
            rows.append({"Model": dn, "Cost/Query": f"${cpq:.6f}", "Daily": f"${daily:,.2f}",
                         "Monthly": f"${daily * 30:,.2f}", "Annual": f"${daily * 365:,.2f}"})
        st.dataframe(rows, use_container_width=True, hide_index=True)
        st.bar_chart({r["Model"]: float(r["Monthly"].replace("$", "").replace(",", "")) for r in rows})


# ═════════════════════════════════════════════════════════════════════════════
# 6. PII SCANNER
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🔍 PII Scanner":
    st.title("🔍 PII Leakage Scanner")
    from evaluators.safety.pii_leakage import PIILeakageEvaluator, PII_PATTERNS
    import re

    sample = (
        "Please contact John at john.doe@example.com or call 555-123-4567.\n"
        "His SSN is 123-45-6789 and card number is 4111 1111 1111 1111."
    )
    text = st.text_area("Paste text to scan", value=sample, height=150)

    if st.button("Scan for PII"):
        result = PIILeakageEvaluator("test").evaluate([{"output": text}])
        c1, c2 = st.columns(2)
        c1.metric("Leakage Rate", f"{result['pii_leakage_rate']:.0%}")
        for pii_type, count in result["detections"].items():
            c2.metric(pii_type.replace("_", " ").title(), count)

        highlighted = text
        for pattern in PII_PATTERNS.values():
            highlighted = re.sub(pattern, lambda m: f"**:red[{m.group()}]**", highlighted)
        st.markdown(highlighted)
