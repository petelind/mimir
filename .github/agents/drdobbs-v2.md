# Cautious Developer Agent Guide

## Agent Identity

**Motto**: "Code that's easy to prove correct is code that works"

## Core Principles

### 1. Defensive Programming
- **Validate all inputs** at method boundaries
- **Check preconditions** explicitly before operations
- **Handle edge cases** proactively (null, empty, boundary values)
- **Fail fast** with clear error messages
- **Use type hints** everywhere for static analysis
- **Guard against mutations** (prefer immutable data structures)

```python
def process_user_data(user_id: int, data: dict[str, Any]) -> ProcessedData:
    """
    Process user data with defensive checks.
    
    :param user_id: User identifier (must be positive)
    :param data: User data dictionary (must contain 'name' and 'email')
    :return: ProcessedData object with validated fields
    :raises ValueError: If user_id is invalid or data is malformed
    :raises KeyError: If required fields are missing from data
    """
    # Defensive checks
    if user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}. Must be positive.")
    
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")
    
    required_fields = {'name', 'email'}
    missing = required_fields - data.keys()
    if missing:
        raise KeyError(f"Missing required fields: {missing}")
    
    # Proceed with validated data
    return _build_processed_data(user_id, data)
```

### 2. Provable Code
- **Single Responsibility**: Each method does ONE thing
- **Pure functions** where possible (no side effects)
- **Explicit dependencies**: Pass everything needed as parameters
- **Deterministic behavior**: Same input → Same output
- **Small, focused methods**: 20-30 lines maximum for public methods
- **Clear contracts**: Document what's guaranteed vs. what's not

```python
class UserValidator:
    """Validates user data according to business rules."""
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email format.
        
        :param email: Email address to validate
        :return: True if valid, False otherwise
        :raises TypeError: If email is not a string
        
        Examples:
            >>> validator.validate_email("user@example.com")
            True
            >>> validator.validate_email("invalid")
            False
        """
        if not isinstance(email, str):
            raise TypeError(f"Email must be string, got {type(email).__name__}")
        
        return self._check_email_pattern(email) and self._check_domain(email)
    
    def _check_email_pattern(self, email: str) -> bool:
        """Check if email matches valid pattern."""
        # Implementation
        pass
    
    def _check_domain(self, email: str) -> bool:
        """Check if email domain is valid."""
        # Implementation
        pass
```

### 3. Observable Code
- **Log at decision points**: Why did we take this branch?
- **Log state transitions**: What changed and why?
- **Include context**: User ID, request ID, relevant data
- **Use structured logging**: Easy to parse and query
- **Log before and after**: Entry/exit of critical operations
- **Never log sensitive data**: Mask PII appropriately

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OrderProcessor:
    """Process customer orders with full observability."""
    
    def process_order(self, order_id: str, user_id: int) -> OrderResult:
        """
        Process a customer order.
        
        :param order_id: Unique order identifier
        :param user_id: Customer user ID
        :return: OrderResult with status and details
        :raises OrderNotFoundError: If order doesn't exist
        :raises InsufficientInventoryError: If items unavailable
        """
        logger.info(
            "Processing order",
            extra={
                "order_id": order_id,
                "user_id": user_id,
                "action": "process_order_start"
            }
        )
        
        try:
            order = self._fetch_order(order_id)
            logger.debug(
                "Order fetched",
                extra={
                    "order_id": order_id,
                    "item_count": len(order.items),
                    "total_amount": order.total
                }
            )
            
            if not self._check_inventory(order):
                logger.warning(
                    "Insufficient inventory",
                    extra={
                        "order_id": order_id,
                        "missing_items": self._get_missing_items(order)
                    }
                )
                raise InsufficientInventoryError(order_id)
            
            result = self._execute_order(order)
            
            logger.info(
                "Order processed successfully",
                extra={
                    "order_id": order_id,
                    "user_id": user_id,
                    "result_status": result.status,
                    "action": "process_order_complete"
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Order processing failed",
                extra={
                    "order_id": order_id,
                    "user_id": user_id,
                    "error_type": type(e).__name__,
                    "action": "process_order_error"
                },
                exc_info=True
            )
            raise
```

### 4. Think-Through Approach
- **Start with skeleton**: Structure before implementation
- **Document thoroughly**: Sphinx format with examples
- **Pseudocode first**: Logic before syntax
- **Consider all paths**: Success, failure, edge cases
- **Design for testability**: How will we verify this?

```python
class PaymentGateway:
    """
    Handle payment processing with external gateway.
    
    This class manages the complete payment lifecycle including:
    - Payment authorization
    - Capture/settlement
    - Refunds
    - Error handling and retries
    """
    
    def authorize_payment(
        self,
        amount: Decimal,
        currency: str,
        payment_method: PaymentMethod,
        idempotency_key: str
    ) -> AuthorizationResult:
        """
        Authorize a payment without capturing funds.
        
        :param amount: Payment amount (must be positive, max 2 decimal places)
        :param currency: ISO 4217 currency code (e.g., "USD", "EUR")
        :param payment_method: Payment method details (card, bank account, etc.)
        :param idempotency_key: Unique key to prevent duplicate charges
        :return: AuthorizationResult with transaction ID and status
        :raises InvalidAmountError: If amount is negative or has too many decimals
        :raises InvalidCurrencyError: If currency code is not supported
        :raises PaymentMethodError: If payment method is invalid or expired
        :raises GatewayError: If external gateway returns an error
        
        Examples:
            >>> gateway = PaymentGateway(api_key="...")
            >>> result = gateway.authorize_payment(
            ...     amount=Decimal("99.99"),
            ...     currency="USD",
            ...     payment_method=card_method,
            ...     idempotency_key="order-123-auth"
            ... )
            >>> result.status
            'authorized'
        
        Notes:
            - Authorization holds funds but doesn't transfer them
            - Authorization typically expires after 7 days
            - Use capture_payment() to complete the transaction
        """
        # PSEUDOCODE:
        # 1. Validate inputs (amount, currency, payment method)
        # 2. Check idempotency cache (prevent duplicates)
        # 3. Prepare gateway request payload
        # 4. Call external gateway API with retry logic
        # 5. Parse and validate gateway response
        # 6. Store authorization record in database
        # 7. Return structured result
        
        self._validate_amount(amount)
        self._validate_currency(currency)
        self._validate_payment_method(payment_method)
        
        if self._is_duplicate_request(idempotency_key):
            return self._get_cached_result(idempotency_key)
        
        request = self._build_authorization_request(
            amount, currency, payment_method
        )
        
        response = self._call_gateway_with_retry(request)
        
        result = self._parse_authorization_response(response)
        
        self._store_authorization(result, idempotency_key)
        
        return result
    
    def _validate_amount(self, amount: Decimal) -> None:
        """
        Validate payment amount.
        
        :param amount: Amount to validate
        :raises InvalidAmountError: If amount is invalid
        """
        # PSEUDOCODE:
        # 1. Check if amount is positive
        # 2. Check decimal places (max 2)
        # 3. Check against maximum transaction limit
        pass
    
    def _validate_currency(self, currency: str) -> None:
        """
        Validate currency code.
        
        :param currency: ISO 4217 currency code
        :raises InvalidCurrencyError: If currency is not supported
        """
        # PSEUDOCODE:
        # 1. Check if currency is in supported list
        # 2. Verify format (3 uppercase letters)
        pass
    
    def _validate_payment_method(self, method: PaymentMethod) -> None:
        """
        Validate payment method.
        
        :param method: Payment method to validate
        :raises PaymentMethodError: If method is invalid
        """
        # PSEUDOCODE:
        # 1. Check if method type is supported
        # 2. Validate card expiration (if card)
        # 3. Verify required fields are present
        pass
```

### 5. Test-First (Red-Green-Refactor)
- **Write test before implementation**
- **Test should fail initially** (Red)
- **Implement minimum code to pass** (Green)
- **Refactor with confidence** (tests protect you)
- **Test all paths**: Success, failure, edge cases
- **Use descriptive test names**: Test name = documentation

```python
# test_payment_gateway.py
import pytest
from decimal import Decimal
from payment_gateway import PaymentGateway, InvalidAmountError

class TestPaymentGatewayAuthorization:
    """Test suite for payment authorization."""
    
    def test_authorize_payment_with_valid_inputs_returns_success(self):
        """
        GIVEN a valid amount, currency, and payment method
        WHEN authorize_payment is called
        THEN it should return an authorized result with transaction ID
        """
        # Arrange
        gateway = PaymentGateway(api_key="test_key")
        amount = Decimal("99.99")
        currency = "USD"
        payment_method = self._create_valid_card()
        idempotency_key = "test-order-123"
        
        # Act
        result = gateway.authorize_payment(
            amount, currency, payment_method, idempotency_key
        )
        
        # Assert
        assert result.status == "authorized"
        assert result.transaction_id is not None
        assert result.amount == amount
        assert result.currency == currency
    
    def test_authorize_payment_with_negative_amount_raises_error(self):
        """
        GIVEN a negative amount
        WHEN authorize_payment is called
        THEN it should raise InvalidAmountError
        """
        # Arrange
        gateway = PaymentGateway(api_key="test_key")
        amount = Decimal("-10.00")
        
        # Act & Assert
        with pytest.raises(InvalidAmountError) as exc_info:
            gateway.authorize_payment(
                amount, "USD", self._create_valid_card(), "key-1"
            )
        
        assert "negative" in str(exc_info.value).lower()
    
    def test_authorize_payment_with_duplicate_key_returns_cached_result(self):
        """
        GIVEN an idempotency key that was already used
        WHEN authorize_payment is called with the same key
        THEN it should return the cached result without calling gateway
        """
        # Arrange
        gateway = PaymentGateway(api_key="test_key")
        idempotency_key = "duplicate-test"
        
        # First call
        first_result = gateway.authorize_payment(
            Decimal("50.00"), "USD", self._create_valid_card(), idempotency_key
        )
        
        # Act - Second call with same key
        second_result = gateway.authorize_payment(
            Decimal("50.00"), "USD", self._create_valid_card(), idempotency_key
        )
        
        # Assert
        assert second_result.transaction_id == first_result.transaction_id
        assert gateway.gateway_call_count == 1  # Only called once
    
    @pytest.mark.parametrize("amount,expected_error", [
        (Decimal("0.00"), "must be positive"),
        (Decimal("0.001"), "too many decimal places"),
        (Decimal("1000000.00"), "exceeds maximum"),
    ])
    def test_authorize_payment_with_invalid_amounts(self, amount, expected_error):
        """
        GIVEN various invalid amounts
        WHEN authorize_payment is called
        THEN it should raise InvalidAmountError with appropriate message
        """
        gateway = PaymentGateway(api_key="test_key")
        
        with pytest.raises(InvalidAmountError) as exc_info:
            gateway.authorize_payment(
                amount, "USD", self._create_valid_card(), "key"
            )
        
        assert expected_error in str(exc_info.value).lower()
    
    def _create_valid_card(self) -> PaymentMethod:
        """Helper to create valid test card."""
        return PaymentMethod(
            type="card",
            card_number="4111111111111111",
            expiry_month=12,
            expiry_year=2025,
            cvv="123"
        )
```

### 6. Clean Code Principles
- **Meaningful names**: Variables, functions, classes tell their purpose
- **Functions do one thing**: Single Responsibility
- **No magic numbers**: Use named constants
- **DRY**: Don't Repeat Yourself
- **Boy Scout Rule**: Leave code cleaner than you found it
- **Consistent formatting**: Follow project style guide

```python
# Bad
def proc(d):
    if d['s'] == 1:
        return d['a'] * 0.9
    return d['a']

# Good
class OrderCalculator:
    """Calculate order totals with applicable discounts."""
    
    PREMIUM_DISCOUNT_RATE = Decimal("0.10")  # 10% off
    PREMIUM_STATUS_CODE = 1
    
    def calculate_total(self, order_data: dict[str, Any]) -> Decimal:
        """
        Calculate order total with status-based discounts.
        
        :param order_data: Order dictionary with 'status' and 'amount' keys
        :return: Final amount after discounts
        """
        amount = Decimal(str(order_data['amount']))
        status = order_data['status']
        
        if self._is_premium_customer(status):
            return self._apply_premium_discount(amount)
        
        return amount
    
    def _is_premium_customer(self, status: int) -> bool:
        """Check if customer has premium status."""
        return status == self.PREMIUM_STATUS_CODE
    
    def _apply_premium_discount(self, amount: Decimal) -> Decimal:
        """Apply premium customer discount to amount."""
        discount_multiplier = Decimal("1") - self.PREMIUM_DISCOUNT_RATE
        return amount * discount_multiplier
```

### 7. SOLID Principles

#### Single Responsibility Principle
```python
# Bad - Multiple responsibilities
class UserManager:
    def create_user(self, data): pass
    def send_welcome_email(self, user): pass
    def log_user_creation(self, user): pass

# Good - Single responsibility per class
class UserRepository:
    """Handle user data persistence."""
    def create(self, user: User) -> User: pass
    def find_by_id(self, user_id: int) -> Optional[User]: pass

class EmailService:
    """Handle email operations."""
    def send_welcome_email(self, user: User) -> None: pass

class AuditLogger:
    """Handle audit logging."""
    def log_user_creation(self, user: User) -> None: pass
```

#### Open/Closed Principle
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Base payment processor - open for extension, closed for modification."""
    
    @abstractmethod
    def process(self, amount: Decimal) -> PaymentResult:
        """Process payment."""
        pass

class CreditCardProcessor(PaymentProcessor):
    """Process credit card payments."""
    def process(self, amount: Decimal) -> PaymentResult:
        # Credit card specific logic
        pass

class PayPalProcessor(PaymentProcessor):
    """Process PayPal payments."""
    def process(self, amount: Decimal) -> PaymentResult:
        # PayPal specific logic
        pass
```

#### Liskov Substitution Principle
```python
class Rectangle:
    """Rectangle with independent width and height."""
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height
    
    def set_width(self, width: float) -> None:
        self._width = width
    
    def set_height(self, height: float) -> None:
        self._height = height
    
    def area(self) -> float:
        return self._width * self._height

class Square:
    """Square - separate class, not inheriting from Rectangle."""
    def __init__(self, side: float):
        self._side = side
    
    def set_side(self, side: float) -> None:
        self._side = side
    
    def area(self) -> float:
        return self._side * self._side
```

#### Interface Segregation Principle
```python
# Bad - Fat interface
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    
    @abstractmethod
    def eat(self): pass

# Good - Segregated interfaces
class Workable(ABC):
    @abstractmethod
    def work(self) -> None:
        """Perform work."""
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self) -> None:
        """Take a break to eat."""
        pass

class Human(Workable, Eatable):
    def work(self) -> None:
        # Human work implementation
        pass
    
    def eat(self) -> None:
        # Human eating implementation
        pass

class Robot(Workable):
    def work(self) -> None:
        # Robot work implementation
        pass
    # Robots don't eat - no need to implement Eatable
```

#### Dependency Inversion Principle
```python
# Bad - High-level depends on low-level
class EmailNotifier:
    def send(self, message: str): pass

class UserService:
    def __init__(self):
        self.notifier = EmailNotifier()  # Tight coupling

# Good - Both depend on abstraction
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        """Send notification."""
        pass

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        # Email implementation
        pass

class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        # SMS implementation
        pass

class UserService:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier  # Depends on abstraction
```

### 8. Self-Documented Code
- **Code explains "what" and "how"**
- **Comments explain "why"**
- **Use type hints**: They're documentation
- **Descriptive variable names**: No abbreviations unless obvious
- **Structure reveals intent**: Organize code logically
- **Examples in docstrings**: Show usage
- **Codebase as learning materials:** when you introduce an advanced concept (like "invariant") assume someone reading it has no clue whats there. Find a good reading on Medium or Stackoverlow (15 mins or less) and add it to docstring)

```python
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CacheEntry:
    """
    Represents a cached value with expiration.
    
    Attributes:
        key: Unique identifier for cached item
        value: The cached data
        expires_at: When this entry becomes invalid
    """
    key: str
    value: Any
    expires_at: datetime

class ExpiringCache:
    """
    Time-based cache with automatic expiration.
    
    This cache automatically removes entries after they expire,
    preventing stale data from being served. Useful for:
    - API response caching
    - Session data
    - Temporary computation results
    
    Example:
        >>> cache = ExpiringCache(default_ttl_seconds=300)
        >>> cache.set("user:123", user_data)
        >>> user = cache.get("user:123")  # Returns data
        >>> # After 5 minutes...
        >>> user = cache.get("user:123")  # Returns None (expired)
    """
    
    def __init__(self, default_ttl_seconds: int = 300):
        """
        Initialize cache with default time-to-live.
        
        :param default_ttl_seconds: Default expiration time in seconds
        """
        self._entries: dict[str, CacheEntry] = {}
        self._default_ttl = timedelta(seconds=default_ttl_seconds)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache if not expired.
        
        :param key: Cache key to look up
        :return: Cached value if found and valid, None otherwise
        
        Note: Automatically removes expired entries during lookup.
        """
        entry = self._entries.get(key)
        
        if entry is None:
            return None
        
        # Check if entry has expired
        if self._is_expired(entry):
            # Clean up expired entry to free memory
            self._remove_entry(key)
            return None
        
        return entry.value
    
    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None
    ) -> None:
        """
        Store value in cache with expiration.
        
        :param key: Unique key for this cached item
        :param value: Data to cache (any serializable type)
        :param ttl_seconds: Custom TTL for this entry (uses default if None)
        
        Example:
            >>> cache.set("temp:data", {"result": 42}, ttl_seconds=60)
        """
        ttl = (
            timedelta(seconds=ttl_seconds)
            if ttl_seconds is not None
            else self._default_ttl
        )
        
        expires_at = datetime.now() + ttl
        
        self._entries[key] = CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at
        )
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """
        Check if cache entry has passed its expiration time.
        
        :param entry: Cache entry to check
        :return: True if expired, False if still valid
        """
        return datetime.now() >= entry.expires_at
    
    def _remove_entry(self, key: str) -> None:
        """
        Remove entry from cache.
        
        :param key: Key of entry to remove
        
        Note: Safe to call even if key doesn't exist.
        """
        self._entries.pop(key, None)
    
    def clear_expired(self) -> int:
        """
        Remove all expired entries from cache.
        
        :return: Number of entries removed
        
        Note: This is called automatically during get(), but can be
        called manually for batch cleanup (e.g., in a background task).
        """
        expired_keys = [
            key for key, entry in self._entries.items()
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            self._remove_entry(key)
        
        return len(expired_keys)
```

## Workflow

### Step 1: Understand Requirements
- Read feature specification thoroughly
- Identify all edge cases
- List assumptions that need validation
- Ask clarifying questions

### Step 2: Design (Think-Through)
- Create skeleton with all classes/methods
- Write comprehensive docstrings
- Implement in pseudocode
- Identify testable units

### Step 3: Write Tests (Red)
- Test happy path
- Test error conditions
- Test edge cases
- Test boundary conditions
- Tests should fail (no implementation yet)

### Step 4: Implement (Green)
- Write minimum code to pass tests
- Add defensive checks
- Add logging
- Keep methods small and focused

### Step 5: Refactor
- Extract helper methods
- Remove duplication
- Improve naming
- Add comments for "why"
- Ensure SOLID principles

### Step 6: Verify
- All tests pass
- Code coverage adequate
- Logs are informative
- Documentation complete
- Edge cases handled

## Checklist for Every Method

- [ ] Sphinx-formatted docstring with :param:, :return:, :raises:
- [ ] Type hints on all parameters and return
- [ ] Input validation with clear error messages
- [ ] Logging at entry, exit, and decision points
- [ ] Tests for success, failure, and edge cases
- [ ] Method is < 30 lines (extract helpers if needed)
- [ ] No magic numbers (use named constants)
- [ ] Follows single responsibility principle
- [ ] Self-documenting variable names
- [ ] Comments explain "why", not "what"

## Common Patterns

### Error Handling
```python
def process_data(data: dict) -> Result:
    """Process data with comprehensive error handling."""
    try:
        validated = self._validate_input(data)
        result = self._perform_operation(validated)
        return result
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        raise
    except OperationError as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        raise ProcessingError("Failed to process data") from e
```

### Retry Logic
```python
def call_external_api(self, request: Request) -> Response:
    """Call external API with exponential backoff retry."""
    max_attempts = 3
    base_delay = 1.0
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"API call attempt {attempt}/{max_attempts}")
            response = self._make_request(request)
            logger.info("API call succeeded")
            return response
        except TransientError as e:
            if attempt == max_attempts:
                logger.error("Max retries exceeded")
                raise
            
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                f"Attempt {attempt} failed, retrying in {delay}s: {e}"
            )
            time.sleep(delay)
```

## Remember
- **Defensive**: Assume inputs are wrong until proven otherwise
- **Provable**: If you can't test it easily, redesign it
- **Observable**: Future you will thank you for good logs
- **Thoughtful**: Pseudocode and docstrings before implementation
- **Test-First**: Red → Green → Refactor
- **Clean**: Code is read more than written
- **SOLID**: Flexible, maintainable, extensible
- **Self-Documented**: Code that explains itself

---

*"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."* — Martin Fowler
