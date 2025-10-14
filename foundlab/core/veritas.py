import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid

@dataclass
class VeritasEvent:
    """
    Representa um único evento na trilha de auditoria do Veritas Protocol.
    """
    decisionId: str
    eventType: str
    payloadHash: str
    timestamp: str
    previousChainHash: Optional[str]
    meta: Optional[Dict[str, Any]] = None
    chainHash: Optional[str] = None

    def __post_init__(self):
        """Calcula o chainHash após a inicialização do objeto."""
        if self.chainHash is None:
            self.chainHash = self._calculate_chain_hash()

    def _calculate_chain_hash(self) -> str:
        """
        Calcula o hash SHA-256 da cadeia de eventos, garantindo a imutabilidade.
        O hash é calculado sobre uma representação JSON ordenada e canônica do evento.
        """
        # O chainHash não entra no seu próprio cálculo
        event_data = {
            "decisionId": self.decisionId,
            "timestamp": self.timestamp,
            "eventType": self.eventType,
            "payloadHash": self.payloadHash,
            "previousChainHash": self.previousChainHash,
        }
        
        # Usar dumps com sort_keys=True para garantir uma representação canônica
        event_string = json.dumps(event_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(event_string.encode('utf-8')).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Converte o evento para um dicionário, ideal para serialização."""
        return asdict(self)

def create_genesis_event(decisionId: str, eventType: str, payload: Dict[str, Any], meta: Optional[Dict[str, Any]] = None) -> VeritasEvent:
    """
    Cria o primeiro evento (genesis) para uma nova decisão.
    """
    payload_string = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    payload_hash = hashlib.sha256(payload_string.encode('utf-8')).hexdigest()
    
    return VeritasEvent(
        decisionId=decisionId,
        eventType=eventType,
        payloadHash=payload_hash,
        timestamp=datetime.now(timezone.utc).isoformat(),
        previousChainHash=None, # O primeiro evento não tem antecessor
        meta=meta
    )

def create_next_event(previous_event: VeritasEvent, eventType: str, payload: Dict[str, Any], meta: Optional[Dict[str, Any]] = None) -> VeritasEvent:
    """
    Cria um evento subsequente, encadeado ao evento anterior.
    """
    if not previous_event.chainHash:
        raise ValueError("O evento anterior deve ter um chainHash calculado.")

    payload_string = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    payload_hash = hashlib.sha256(payload_string.encode('utf-8')).hexdigest()

    return VeritasEvent(
        decisionId=previous_event.decisionId,
        eventType=eventType,
        payloadHash=payload_hash,
        timestamp=datetime.now(timezone.utc).isoformat(),
        previousChainHash=previous_event.chainHash,
        meta=meta
    )

def generate_decision_id() -> str:
    """Gera um novo UUID v4 para ser usado como DecisionID."""
    return str(uuid.uuid4())
