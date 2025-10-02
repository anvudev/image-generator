"""
Test Numeric Sort for History Names
Kiểm tra logic sort name dạng số
"""
from app.utils.helpers import sort_histories_by_name, parse_numeric_string


def test_parse_numeric_string():
    """Test parse string to number"""
    print("🧪 Test parse_numeric_string")
    
    # Test numeric strings
    assert parse_numeric_string("4") == 4.0
    assert parse_numeric_string("41") == 41.0
    assert parse_numeric_string("51") == 51.0
    assert parse_numeric_string("3.14") == 3.14
    
    # Test non-numeric strings
    assert parse_numeric_string("abc") == 0.0
    assert parse_numeric_string("") == 0.0
    assert parse_numeric_string("level_4") == 0.0
    
    print("✅ parse_numeric_string tests passed")


def test_sort_histories_numeric():
    """Test sort histories với numeric names"""
    print("\n🧪 Test sort_histories_by_name (numeric)")
    
    # Sample histories với numeric names
    histories = [
        {"value": {"name": "51"}},
        {"value": {"name": "4"}},
        {"value": {"name": "41"}},
        {"value": {"name": "5"}},
        {"value": {"name": "100"}},
    ]
    
    # Test ascending
    sorted_asc = sort_histories_by_name(histories, "asc")
    names_asc = [h["value"]["name"] for h in sorted_asc]
    print(f"  Ascending: {names_asc}")
    assert names_asc == ["4", "5", "41", "51", "100"]
    
    # Test descending
    sorted_desc = sort_histories_by_name(histories, "desc")
    names_desc = [h["value"]["name"] for h in sorted_desc]
    print(f"  Descending: {names_desc}")
    assert names_desc == ["100", "51", "41", "5", "4"]
    
    print("✅ Numeric sort tests passed")


def test_sort_histories_text():
    """Test sort histories với text names"""
    print("\n🧪 Test sort_histories_by_name (text)")
    
    # Sample histories với text names
    histories = [
        {"value": {"name": "Level C"}},
        {"value": {"name": "Level A"}},
        {"value": {"name": "Level B"}},
    ]
    
    # Test ascending
    sorted_asc = sort_histories_by_name(histories, "asc")
    names_asc = [h["value"]["name"] for h in sorted_asc]
    print(f"  Ascending: {names_asc}")
    assert names_asc == ["Level A", "Level B", "Level C"]
    
    # Test descending
    sorted_desc = sort_histories_by_name(histories, "desc")
    names_desc = [h["value"]["name"] for h in sorted_desc]
    print(f"  Descending: {names_desc}")
    assert names_desc == ["Level C", "Level B", "Level A"]
    
    print("✅ Text sort tests passed")


def test_sort_histories_mixed():
    """Test sort histories với mixed numeric và text names"""
    print("\n🧪 Test sort_histories_by_name (mixed)")
    
    # Sample histories với mixed names
    histories = [
        {"value": {"name": "Level A"}},
        {"value": {"name": "51"}},
        {"value": {"name": "4"}},
        {"value": {"name": "Level B"}},
        {"value": {"name": "41"}},
    ]
    
    # Test ascending - số trước, text sau
    sorted_asc = sort_histories_by_name(histories, "asc")
    names_asc = [h["value"]["name"] for h in sorted_asc]
    print(f"  Ascending: {names_asc}")
    # Numeric values (4, 41, 51) should come before text values
    assert names_asc[0] == "4"
    assert names_asc[1] == "41"
    assert names_asc[2] == "51"
    assert "Level A" in names_asc
    assert "Level B" in names_asc
    
    # Test descending
    sorted_desc = sort_histories_by_name(histories, "desc")
    names_desc = [h["value"]["name"] for h in sorted_desc]
    print(f"  Descending: {names_desc}")
    
    print("✅ Mixed sort tests passed")


def test_sort_histories_edge_cases():
    """Test edge cases"""
    print("\n🧪 Test edge cases")
    
    # Empty list
    assert sort_histories_by_name([], "asc") == []
    
    # Single item
    single = [{"value": {"name": "4"}}]
    assert sort_histories_by_name(single, "asc") == single
    
    # Missing name field
    missing_name = [
        {"value": {"name": "4"}},
        {"value": {}},  # Missing name
        {"value": {"name": "5"}},
    ]
    sorted_missing = sort_histories_by_name(missing_name, "asc")
    assert len(sorted_missing) == 3
    
    print("✅ Edge case tests passed")


def test_real_world_scenario():
    """Test với scenario thực tế"""
    print("\n🧪 Test real-world scenario")
    
    # Giống như data thực tế: "4", "41", "51"
    histories = [
        {
            "_id": "id1",
            "key": "history",
            "value": {
                "id": "level_1",
                "name": "41",
                "level": {"config": {"difficulty": "Hard"}},
                "createdAt": "2025-01-01T00:00:00Z",
                "updatedAt": "2025-01-01T00:00:00Z"
            },
            "updatedAt": "2025-01-01T00:00:00Z"
        },
        {
            "_id": "id2",
            "key": "history",
            "value": {
                "id": "level_2",
                "name": "4",
                "level": {"config": {"difficulty": "Easy"}},
                "createdAt": "2025-01-02T00:00:00Z",
                "updatedAt": "2025-01-02T00:00:00Z"
            },
            "updatedAt": "2025-01-02T00:00:00Z"
        },
        {
            "_id": "id3",
            "key": "history",
            "value": {
                "id": "level_3",
                "name": "51",
                "level": {"config": {"difficulty": "Medium"}},
                "createdAt": "2025-01-03T00:00:00Z",
                "updatedAt": "2025-01-03T00:00:00Z"
            },
            "updatedAt": "2025-01-03T00:00:00Z"
        },
        {
            "_id": "id4",
            "key": "history",
            "value": {
                "id": "level_4",
                "name": "5",
                "level": {"config": {"difficulty": "Easy"}},
                "createdAt": "2025-01-04T00:00:00Z",
                "updatedAt": "2025-01-04T00:00:00Z"
            },
            "updatedAt": "2025-01-04T00:00:00Z"
        }
    ]
    
    # Sort ascending
    sorted_asc = sort_histories_by_name(histories, "asc")
    names_asc = [h["value"]["name"] for h in sorted_asc]
    print(f"  Real-world ascending: {names_asc}")
    assert names_asc == ["4", "5", "41", "51"], f"Expected ['4', '5', '41', '51'], got {names_asc}"
    
    # Sort descending
    sorted_desc = sort_histories_by_name(histories, "desc")
    names_desc = [h["value"]["name"] for h in sorted_desc]
    print(f"  Real-world descending: {names_desc}")
    assert names_desc == ["51", "41", "5", "4"], f"Expected ['51', '41', '5', '4'], got {names_desc}"
    
    print("✅ Real-world scenario tests passed")


if __name__ == "__main__":
    print("🧪 Testing Numeric Sort Logic\n")
    print("="*60)
    
    try:
        test_parse_numeric_string()
        test_sort_histories_numeric()
        test_sort_histories_text()
        test_sort_histories_mixed()
        test_sort_histories_edge_cases()
        test_real_world_scenario()
        
        print("\n" + "="*60)
        print("🎉 All tests passed!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

