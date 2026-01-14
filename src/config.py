"""
Configuration management module
Loads and provides access to configuration settings
"""
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for the churn prediction project"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config file. If None, uses default path.
        """
        if config_path is None:
            # Default path relative to project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / 'config' / 'config.yaml'
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key (supports nested keys with dots, e.g., 'data.test_size')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_data_config(self) -> Dict[str, Any]:
        """Get data configuration"""
        return self.config.get('data', {})
    
    def get_preprocessing_config(self) -> Dict[str, Any]:
        """Get preprocessing configuration"""
        return self.config.get('preprocessing', {})
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration"""
        return self.config.get('model', {})
    
    def get_training_config(self) -> Dict[str, Any]:
        """Get training configuration"""
        return self.config.get('training', {})
    
    def get_features_config(self) -> Dict[str, Any]:
        """Get feature engineering configuration"""
        return self.config.get('features', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output paths configuration"""
        return self.config.get('output', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.config.get('logging', {})
    
    def __repr__(self) -> str:
        return f"Config(config_path='{self.config_path}')"


# Global config instance
_config = None


def get_config(config_path: str = None) -> Config:
    """
    Get global configuration instance
    
    Args:
        config_path: Path to config file. If None, uses default path.
        
    Returns:
        Config instance
    """
    global _config
    
    if _config is None or config_path is not None:
        _config = Config(config_path)
    
    return _config


if __name__ == "__main__":
    # Example usage
    config = get_config()
    
    print("Data config:", config.get_data_config())
    print("Test size:", config.get('data.test_size'))
    print("Model type:", config.get('model.type'))
    print("XGBoost params:", config.get('model.params.xgboost'))
