import main


def test_main_runs_preflight_before_pipeline(monkeypatch):
    calls = []

    def fake_validate_config(config):
        calls.append(("preflight", config))

    class FakePipeline:
        def __init__(self, config):
            calls.append(("pipeline_init", config))

        def run(self):
            calls.append(("pipeline_run", None))

    monkeypatch.setattr(main, "validate_config", fake_validate_config)
    monkeypatch.setattr(main, "Pipeline", FakePipeline)

    main.main()

    assert [name for name, _ in calls] == [
        "preflight",
        "pipeline_init",
        "pipeline_run",
    ]
