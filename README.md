# Agaru Up Beacon - Raspberry Pi 4B iBeacon

Raspberry Pi 4BでiBeacon形式のBLEビーコンをブロードキャストするアプリケーションです。UUIDをブロードキャストして、周辺のデバイスに検出されるようにします。

## 要件

- Raspberry Pi 4B（またはBluetoothを搭載したRaspberry Pi）
- Python 3.9以上
- BluetoothハードウェアとBlueZ（Linux Bluetooth stack）

## インストール

### 1. 必要なパッケージのインストール

```bash
sudo apt-get update
sudo apt-get install bluez python3-pip python3-venv
```

### 2. Pythonプロジェクトの依存関係をインストール

```bash
# 仮想環境を作成（オプション）
python3 -m venv .venv
source .venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
# または
uv sync
```

## 設定

[main.py](main.py)の以下のパラメータをカスタマイズできます：

```python
UUID = "12345678-1234-1234-1234-123456789012"  # iBeaconのUUID
MAJOR = 1                                        # Major値（0-65535）
MINOR = 1                                        # Minor値（0-65535）
TX_POWER = -50                                   # 送信電力（dBm）
```

## 実行方法

### Bluetoothを有効にする

```bash
sudo bluetoothctl
```

Bluetoothコンソールで：
```
power on
agent on
exit
```

### ビーコンを開始

```bash
# Root権限が必要です
sudo python main.py
```

## iBeacon仕様

このアプリケーションはAppleのiBeacon形式に準拠しています：

- **Company ID**: 0x004C（Apple Inc.）
- **Type**: 0x02
- **Length**: 0x15（21バイト）
- **UUID**: 128ビット（16バイト）
- **Major**: 16ビット
- **Minor**: 16ビット
- **TX Power**: 8ビット符号付き整数（dBm）

## トラブルシューティング

### エラー: "Permission denied"

Root権限で実行してください：
```bash
sudo python main.py
```

### エラー: "BLE adapter not found"

Bluetoothが有効になっていません：
```bash
sudo bluetoothctl power on
```

### ビーコンが検出されない

1. UUIDが正しく設定されていることを確認
2. 他のBLEスキャナーアプリで確認してみてください
3. Raspberry Piの物理的なBluetoothアンテナが接続されていることを確認

## テスト

iPhone/Androidで専用のiBeacon検出アプリを使用してテストできます：

- **iOS**: "iBeacon Detector"（AppStore）
- **Android**: "Beacon Scanner"（PlayStore）

## ライセンス

MIT

## 参考資料

- [Bleak Documentation](https://bleak.readthedocs.io/)
- [iBeacon Specification](https://developer.apple.com/ibeacon/)
- [BlueZ Documentation](https://github.com/bluez/bluez)
