def test_freeze_uuids_using_fixture(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_freeze_uuids(freeze_uuids):
            import uuid
            assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_marker(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_different_obj_path_and_version(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            obj_path="uuid.uuid1",
            version=1
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid1()) == "00000000-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_with_cycle_side_effect(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            side_effect="cycle",
            values=[
                "11111111-0000-0000-0000-000000000000",
                "22222222-0000-0000-0000-000000000000"
            ]
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "11111111-0000-0000-0000-000000000000"
            assert str(uuid.uuid4()) == "22222222-0000-0000-0000-000000000000"
            assert str(uuid.uuid4()) == "11111111-0000-0000-0000-000000000000"
            assert str(uuid.uuid4()) == "22222222-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_with_values_side_effect(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            side_effect="values",
            values=[
                "11111111-0000-0000-0000-000000000000",
                "22222222-0000-0000-0000-000000000000"
            ]
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "11111111-0000-0000-0000-000000000000"
            assert str(uuid.uuid4()) == "22222222-0000-0000-0000-000000000000"
            with pytest.raises(StopIteration):
                uuid.uuid4()
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_random_side_effect(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            side_effect="random"
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "bdd640fb-0667-4ad1-9c80-317fa3b1799d"
            assert str(uuid.uuid4()) == "23b8c1e9-3924-46de-beb1-3b9046685257"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_random_side_effect_with_different_seed(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            side_effect="random",
            seed=1337
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "b5bab1cd-8884-47a5-acef-e37b9e250d03"
            assert str(uuid.uuid4()) == "bb5d75b8-95f6-48f2-922b-adb05da83cff"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_auto_increment_side_effect(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            side_effect="auto_increment"
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000000"
            assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000001"
            assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000002"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_with_unknown_side_effect(testdir):
    testdir.makepyfile(
        """
        import pytest

        with pytest.raises(ValueError):
            @pytest.mark.freeze_uuids(
                side_effect="foobar",
            )
            def test_freeze_uuids():
                pass
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 2


def test_freeze_uuids_using_included_namespace(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            namespace="uuid"
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_excluded_namespace(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            namespace="foobar"
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) != "00000000-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0
