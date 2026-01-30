from typing import List, Dict, Any

class AIServiceInterface:
    """
    Interface for AI-powered features to be implemented in Phase 3.
    Use this class to define the contract for AI services.
    """
    
    def predict_demand(self, item_id: int) -> Dict[str, Any]:
        """
        Predict demand for a specific inventory item.
        """
        raise NotImplementedError("AI features are not enabled in Phase 2.")

    def generate_restock_plan(self) -> List[Dict[str, Any]]:
        """
        Generate a restocking plan based on current inventory levels and predicted demand.
        """
        raise NotImplementedError("AI features are not enabled in Phase 2.")

# Singleton instance to be used throughout the app
# In Phase 3, this will be replaced by a real implementation
ai_service = AIServiceInterface()
