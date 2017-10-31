# opsdroid skill magpi

A skill for [opsdroid](https://github.com/opsdroid/opsdroid) to notify of new [MagPi](https://www.raspberrypi.org/magpi/) issues.

## Requirements

None.

## Configuration

```yaml
skills:
  - name: magpi
    room: "#raspberrypi"  # (Optional) room to send notifications to
```

## Usage

#### default

This skill checks every hour for new issues of MagPi.

> opsdroid: There's a new issue of MagPi:
>           https://www.raspberrypi.org/magpi-issues/MagPi56.pdf

#### `magpi <number>`

Get the link to an issue by number.

> user: What's the link to magpi 42?
>
> opsdroid: https://www.raspberrypi.org/magpi-issues/MagPi42.pdf
