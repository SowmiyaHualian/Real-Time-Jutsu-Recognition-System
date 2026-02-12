"""
Chakra System Module
Manages chakra energy, consumption, regeneration, and cooldowns
"""

import time


class ChakraSystem:
    """Manages chakra energy and cooldown mechanics"""

    def __init__(self, max_chakra=100, regen_rate=0.5):
        """
        Initialize chakra system

        Args:
            max_chakra: Maximum chakra capacity
            regen_rate: Chakra regeneration per frame
        """
        self.max_chakra = max_chakra
        self.current_chakra = max_chakra
        self.regen_rate = regen_rate

        # Jutsu costs
        self.jutsu_costs = {
            "Fist": 30,
            "Open Palm": 25,
            "Peace Sign": 40,
            "Thumbs Up": 20,
            "Rock Sign": 35,
            "Gun Sign": 30,
            "Three Fingers": 25,
            "Point": 15
        }

        # Cooldown system
        self.cooldowns = {}  # {jutsu_name: end_time}
        self.cooldown_durations = {
            "Fist": 2.0,
            "Open Palm": 3.0,
            "Peace Sign": 4.0,
            "Thumbs Up": 2.0,
            "Rock Sign": 3.5,
            "Gun Sign": 2.5,
            "Three Fingers": 2.0,
            "Point": 1.5
        }

    def can_use_jutsu(self, jutsu_name):
        """
        Check if jutsu can be used (enough chakra and not on cooldown)

        Args:
            jutsu_name: Name of the jutsu

        Returns:
            Boolean indicating if jutsu can be used
        """
        # Check if jutsu exists
        if jutsu_name not in self.jutsu_costs:
            return False

        # Check chakra
        cost = self.jutsu_costs[jutsu_name]
        if self.current_chakra < cost:
            return False

        # Check cooldown
        if jutsu_name in self.cooldowns:
            if time.time() < self.cooldowns[jutsu_name]:
                return False

        return True

    def use_jutsu(self, jutsu_name):
        """
        Consume chakra and start cooldown for jutsu

        Args:
            jutsu_name: Name of the jutsu

        Returns:
            Boolean indicating success
        """
        if not self.can_use_jutsu(jutsu_name):
            return False

        # Consume chakra
        cost = self.jutsu_costs[jutsu_name]
        self.current_chakra -= cost

        # Start cooldown
        cooldown_duration = self.cooldown_durations.get(jutsu_name, 2.0)
        self.cooldowns[jutsu_name] = time.time() + cooldown_duration

        return True

    def regenerate(self):
        """Regenerate chakra over time"""
        if self.current_chakra < self.max_chakra:
            self.current_chakra = min(self.max_chakra, self.current_chakra + self.regen_rate)

    def get_cooldown_remaining(self, jutsu_name):
        """
        Get remaining cooldown time for a jutsu

        Args:
            jutsu_name: Name of the jutsu

        Returns:
            Remaining cooldown time in seconds (0 if ready)
        """
        if jutsu_name not in self.cooldowns:
            return 0.0

        remaining = self.cooldowns[jutsu_name] - time.time()
        return max(0.0, remaining)

    def reset(self):
        """Reset chakra to maximum and clear cooldowns"""
        self.current_chakra = self.max_chakra
        self.cooldowns.clear()

    def get_chakra_percentage(self):
        """Get chakra as percentage"""
        return (self.current_chakra / self.max_chakra) * 100

    def get_chakra_color(self):
        """Get color based on chakra level (for UI)"""
        percentage = self.get_chakra_percentage()
        if percentage > 60:
            return (0, 255, 0)  # Green
        elif percentage > 30:
            return (0, 255, 255)  # Yellow
        else:
            return (0, 0, 255)  # Red