"""Example usage for Tapestry DOLR Skill."""
from client import TapestryRouter

def main():
    print("Executing Tapestry DOLR...")
    router = TapestryRouter("Node_Alpha")
    router.publish_object("OBJECT_MODEL_WEIGHTS_V1", "Replica_Server_99")
    holder = router.route_to_object("OBJECT_MODEL_WEIGHTS_V1")
    print("Located replica server:", holder)
    assert holder == "Replica_Server_99"
    print("Tapestry DOLR verified successfully!")

if __name__ == "__main__":
    main()
