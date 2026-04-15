# Blockchain-Style Integrity Policy

## 대상

Memory Chip Readiness Foundation (`memory-chip-readiness`)

## 해시 알고리즘

SHA-256 (Python `hashlib.sha256`)

## 포함 파일

- `memory_chip_readiness/**/*.py` — 모든 Python 소스
- `memory_chip_readiness/py.typed` — 타입 힌트 마커
- `pyproject.toml` — 프로젝트 메타데이터
- `LICENSE` — 라이선스 전문

## 서명 파일

- `SIGNATURE.sha256` — 파일별 SHA-256 해시 매니페스트

## 검증 방법

```bash
python scripts/generate_signature.py --verify
```

## 블록 로그

각 릴리스마다 [MEMORYCHIP_BLOCKCHAIN_LOG.md](MEMORYCHIP_BLOCKCHAIN_LOG.md)에
블록이 추가된다. 블록에는 버전, 날짜, 주요 변경사항, 테스트 수가 기록된다.

## 보장 범위

이 정책은 **코드 무결성 추적**을 위한 것이며,
암호화 블록체인(분산 원장)과는 다르다.
파일 변조 여부를 SHA-256 해시로 감지할 수 있으나,
분산 합의나 트랜잭션 보증은 포함하지 않는다.
