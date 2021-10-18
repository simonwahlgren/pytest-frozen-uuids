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


def test_freeze_uuids_using_different_value(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            values=["11111111-0000-0000-0000-000000000000"]
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "11111111-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_multiple_values(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            values=[
                "11111111-0000-0000-0000-000000000000",
                "22222222-0000-0000-0000-000000000000"
            ]
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "11111111-0000-0000-0000-000000000000"
            assert str(uuid.uuid4()) == "22222222-0000-0000-0000-000000000000"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_and_cycling_values(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
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


def test_freeze_uuids_with_cycle_disabled(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            cycle=False,
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


def test_freeze_uuids_using_random_genrator(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            random=True
        )
        def test_freeze_uuids():
            import uuid
            assert str(uuid.uuid4()) == "bdd640fb-0667-4ad1-9c80-317fa3b1799d"
            assert str(uuid.uuid4()) == "23b8c1e9-3924-46de-beb1-3b9046685257"
    """
    )
    result = testdir.runpytest("-v", "-s")
    assert result.ret == 0


def test_freeze_uuids_using_random_genrator_with_different_seed(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.freeze_uuids(
            random=True,
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
