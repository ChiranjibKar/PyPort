import sys
import os
import re
import subprocess
import zipfile
from importlib.metadata import distributions

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLabel, QHBoxLayout,
    QLineEdit, QGroupBox, QProgressBar, QDialog,
    QGraphicsDropShadowEffect, QFrame, QSizePolicy,
    QSplitter
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSize
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QColor, QFont, QPainter, QPen,
    QLinearGradient
)


# ══════════════════════════════════════════════════════
#  NEON COLOR PALETTE
# ══════════════════════════════════════════════════════
NEON = {
    "bg_dark":      "#0a0a0f",
    "bg_panel":     "#0d0d14",
    "bg_input":     "#0f0f18",
    "bg_button":    "#111119",
    "cyan":         "#00e5ff",
    "cyan_dim":     "#007a8a",
    "magenta":      "#ff00e5",
    "magenta_dim":  "#8a007a",
    "green":        "#39ff14",
    "green_dim":    "#1a8a0a",
    "orange":       "#ff6e00",
    "red":          "#ff1744",
    "yellow":       "#ffea00",
    "text":         "#e0e8f0",
    "text_dim":     "#6a7a8a",
    "border":       "#1a1a2e",
}


# ══════════════════════════════════════════════════════
#  GENERATE APP ICON
# ══════════════════════════════════════════════════════
def create_app_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    pen = QPen(QColor(NEON["cyan"]), 2)
    painter.setPen(pen)
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(NEON["bg_dark"]))
    painter.drawRoundedRect(8, 8, 48, 48, 8, 8)

    font = QFont("Consolas", 18, QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(QColor(NEON["cyan"]))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Py")

    gradient = QLinearGradient(12, 50, 52, 50)
    gradient.setColorAt(0, QColor(NEON["cyan"]))
    gradient.setColorAt(0.5, QColor(NEON["magenta"]))
    gradient.setColorAt(1, QColor(NEON["green"]))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(gradient)
    painter.drawRoundedRect(14, 48, 36, 3, 1, 1)

    painter.end()
    return QIcon(pixmap)


# ══════════════════════════════════════════════════════
#  NEON DIALOG
# ══════════════════════════════════════════════════════
class NeonDialog(QDialog):
    INFO    = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR   = "error"
    CONFIRM = "confirm"

    THEME = {
        "info":    {"color": NEON["cyan"],   "icon": "ℹ️",  "title": "Info"},
        "success": {"color": NEON["green"],  "icon": "✅", "title": "Success"},
        "warning": {"color": NEON["yellow"], "icon": "⚠️",  "title": "Warning"},
        "error":   {"color": NEON["red"],    "icon": "❌", "title": "Error"},
        "confirm": {"color": NEON["orange"], "icon": "🔥", "title": "Confirm"},
    }

    def __init__(self, parent=None, dialog_type="info", title="", message="", detail=""):
        super().__init__(parent)
        self.result_action = False
        theme = self.THEME.get(dialog_type, self.THEME["info"])
        accent = theme["color"]

        self.setWindowTitle(title or theme["title"])
        self.setFixedWidth(440)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        container = QFrame(self)
        container.setObjectName("dlgBox")
        container.setStyleSheet(f"""
            #dlgBox {{
                background-color: {NEON['bg_panel']};
                border: 1px solid {accent};
                border-radius: 16px;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

        inner = QVBoxLayout(container)
        inner.setContentsMargins(28, 24, 28, 24)
        inner.setSpacing(16)

        top = QHBoxLayout()
        icon_lbl = QLabel(theme["icon"])
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent;")
        top.addWidget(icon_lbl)
        title_lbl = QLabel(title or theme["title"])
        title_lbl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {accent}; background: transparent; font-family: 'Segoe UI';")
        top.addWidget(title_lbl)
        top.addStretch()
        inner.addLayout(top)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background-color: {accent}; max-height: 1px; border: none;")
        inner.addWidget(sep)

        msg = QLabel(message)
        msg.setWordWrap(True)
        msg.setStyleSheet(f"font-size: 13px; color: {NEON['text']}; background: transparent; font-family: 'Segoe UI';")
        inner.addWidget(msg)

        if detail:
            det = QLabel(detail)
            det.setWordWrap(True)
            det.setStyleSheet(f"font-size: 11px; color: {NEON['text_dim']}; background: transparent; padding: 8px 12px; border-left: 2px solid {accent}; font-family: 'Consolas';")
            inner.addWidget(det)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_base = lambda bg, fg: f"""
            QPushButton {{
                background-color: {bg}; color: {fg}; border: none;
                border-radius: 8px; padding: 8px 24px;
                font-size: 12px; font-weight: bold; font-family: 'Segoe UI';
            }}
            QPushButton:hover {{ opacity: 0.85; }}
        """

        if dialog_type == "confirm":
            cancel = QPushButton("Cancel")
            cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            cancel.setStyleSheet(btn_base(NEON["bg_button"], NEON["text_dim"]).replace("border: none", f"border: 1px solid {NEON['border']}"))
            cancel.clicked.connect(self.reject)
            btn_row.addWidget(cancel)

            ok = QPushButton("Confirm")
            ok.setCursor(Qt.CursorShape.PointingHandCursor)
            ok.setStyleSheet(btn_base(accent, NEON["bg_dark"]))
            ok.clicked.connect(self._confirm)
            btn_row.addWidget(ok)
        else:
            ok = QPushButton("Got it")
            ok.setCursor(Qt.CursorShape.PointingHandCursor)
            ok.setStyleSheet(btn_base(accent, NEON["bg_dark"]))
            ok.clicked.connect(self.accept)
            btn_row.addWidget(ok)

        inner.addLayout(btn_row)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(accent))
        shadow.setOffset(0, 0)
        container.setGraphicsEffect(shadow)

    def _confirm(self):
        self.result_action = True
        self.accept()

    @staticmethod
    def show_info(parent, title, message, detail=""):
        NeonDialog(parent, NeonDialog.INFO, title, message, detail).exec()

    @staticmethod
    def show_success(parent, title, message, detail=""):
        NeonDialog(parent, NeonDialog.SUCCESS, title, message, detail).exec()

    @staticmethod
    def show_warning(parent, title, message, detail=""):
        NeonDialog(parent, NeonDialog.WARNING, title, message, detail).exec()

    @staticmethod
    def show_error(parent, title, message, detail=""):
        NeonDialog(parent, NeonDialog.ERROR, title, message, detail).exec()

    @staticmethod
    def ask_confirm(parent, title, message, detail=""):
        d = NeonDialog(parent, NeonDialog.CONFIRM, title, message, detail)
        d.exec()
        return d.result_action


# ══════════════════════════════════════════════════════
#  NEON BUTTON
# ══════════════════════════════════════════════════════
class NeonButton(QPushButton):
    def __init__(self, icon_text, label, accent=NEON["cyan"], parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_text}   {label}")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(38)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {NEON['bg_button']};
                border: 1px solid {NEON['border']};
                border-left: 3px solid {accent};
                border-radius: 8px;
                padding: 4px 14px;
                color: {NEON['text']};
                font-size: 12px;
                font-family: 'Segoe UI', sans-serif;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: #161622;
                border: 1px solid {accent};
                border-left: 3px solid {accent};
                color: {accent};
            }}
            QPushButton:pressed {{
                background-color: #0c0c15;
            }}
        """)


# ══════════════════════════════════════════════════════
#  WORKER THREAD
# ══════════════════════════════════════════════════════
class CommandWorker(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_status = pyqtSignal(bool)
    progress_signal = pyqtSignal(int)

    def __init__(self, command, expected_lines=0):
        super().__init__()
        self.command = command
        self.expected_lines = expected_lines
        self._had_error = False
        self._line_count = 0

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )

            for line in process.stdout:
                stripped = line.rstrip()
                self._line_count += 1
                self.output_signal.emit(stripped)

                # Parse pip percentage from output
                pct_match = re.search(r'(\d+)%', stripped)
                if pct_match:
                    self.progress_signal.emit(int(pct_match.group(1)))
                elif self.expected_lines > 0:
                    pct = min(int(self._line_count / self.expected_lines * 100), 99)
                    self.progress_signal.emit(pct)

            stderr_out = process.stderr.read()
            if stderr_out.strip():
                self.error_signal.emit(stderr_out.strip())
                self._had_error = True

            process.wait()
            if process.returncode != 0:
                self._had_error = True

            self.progress_signal.emit(100)
            self.finished_status.emit(not self._had_error)

        except Exception as e:
            self.error_signal.emit(str(e))
            self.finished_status.emit(False)


# ══════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════
class PackageManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ PyPort — Offline Python Environment Manager")
        self.setGeometry(160, 60, 1020, 800)
        self.setWindowIcon(create_app_icon())
        self.setMinimumSize(780, 550)

        self.init_ui()

        # Typewriter
        self.full_text = "⚡ System Online  ·  Made by Chiranjib Kar"
        self.current_index = 0
        self.type_timer = QTimer()
        self.type_timer.timeout.connect(self.typewriter_effect)
        self.type_timer.start(35)

    def init_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(14, 10, 14, 10)
        root.setSpacing(6)

        # ═══════════ HEADER ═══════════
        header = QLabel("P Y P O R T")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            font-size: 28px; font-weight: bold; color: {NEON['cyan']};
            letter-spacing: 10px; padding: 4px 0 0 0;
            font-family: 'Consolas', 'Cascadia Code', monospace;
        """)
        root.addWidget(header)

        tagline = QLabel("Offline Python Environment Manager")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet(f"""
            font-size: 10px; color: {NEON['text_dim']};
            letter-spacing: 3px; text-transform: uppercase;
            font-family: 'Segoe UI'; padding: 0;
        """)
        root.addWidget(tagline)

        self.subtitle = QLabel("")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setFixedHeight(16)
        self.subtitle.setStyleSheet(f"""
            font-size: 10px; color: {NEON['green']};
            letter-spacing: 1px; font-family: 'Consolas', monospace;
        """)
        root.addWidget(self.subtitle)

        # Gradient separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background: qlineargradient(x1:0, x2:1, stop:0 transparent, stop:0.3 {NEON['cyan_dim']}, stop:0.7 {NEON['magenta_dim']}, stop:1 transparent); border: none;")
        root.addWidget(sep)

        # ═══════════ INPUT ROW ═══════════
        input_row = QHBoxLayout()
        input_row.setSpacing(8)

        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText("📦  Package name   ·   or type CONFIRM for reset")
        self.package_input.setFixedHeight(36)
        self.package_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {NEON['bg_input']};
                border: 1px solid {NEON['border']};
                border-radius: 8px;
                padding: 0 12px;
                color: {NEON['text']};
                font-size: 12px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{ border-color: {NEON['cyan']}; }}
        """)
        input_row.addWidget(self.package_input, stretch=1)

        install_btn = NeonButton("📥", "Install", NEON["green"])
        install_btn.setFixedWidth(120)
        install_btn.clicked.connect(self.install_package)
        input_row.addWidget(install_btn)

        root.addLayout(input_row)

        # ═══════════ SPLITTER: Commands (top) | Terminal (bottom) ═══════════
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(6)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background: qlineargradient(x1:0, x2:1,
                    stop:0 transparent, stop:0.3 {NEON['cyan_dim']},
                    stop:0.7 {NEON['magenta_dim']}, stop:1 transparent);
                height: 3px;
                margin: 3px 60px;
                border-radius: 1px;
            }}
        """)

        # ── TOP HALF: Command Buttons ──
        cmd_panel = QWidget()
        cmd_layout = QVBoxLayout(cmd_panel)
        cmd_layout.setContentsMargins(0, 4, 0, 0)
        cmd_layout.setSpacing(6)

        # COMMON TOOLS
        common_grp = self._make_group("COMMON TOOLS", NEON["cyan"])
        cl = common_grp.layout()
        r1 = QHBoxLayout()
        r1.setSpacing(6)
        self._add_btn(r1, "📋", "Show Installed Modules", self.show_packages, NEON["cyan"])
        self._add_btn(r1, "🐍", "Python Version", self.check_python_version, NEON["cyan"])
        self._add_btn(r1, "📌", "pip Version", self.check_pip_version, NEON["cyan"])
        cl.addLayout(r1)
        cmd_layout.addWidget(common_grp)

        # ONLINE PC
        online_grp = self._make_group("ONLINE PC  ·  Build System", NEON["green"])
        ol = online_grp.layout()
        r2 = QHBoxLayout()
        r2.setSpacing(6)
        self._add_btn(r2, "📝", "Export requirements.txt", self.export_requirements, NEON["green"])
        self._add_btn(r2, "⬇️", "Download Packages", self.download_packages, NEON["green"])
        self._add_btn(r2, "⬆️", "Update pip (Online)", self.update_pip, NEON["green"])
        ol.addLayout(r2)
        r3 = QHBoxLayout()
        r3.setSpacing(6)
        self._add_btn(r3, "📦", "Full Offline Kit", self.prepare_offline_kit, NEON["green"])
        self._add_btn(r3, "⚡", "Smart Export (New Only)", self.smart_export, NEON["green"])
        ol.addLayout(r3)
        cmd_layout.addWidget(online_grp)

        # OFFLINE PC
        offline_grp = self._make_group("OFFLINE PC  ·  Deployment", NEON["magenta"])
        ofl = offline_grp.layout()
        r4 = QHBoxLayout()
        r4.setSpacing(6)
        self._add_btn(r4, "📥", "Install Modules", self.install_from_folder, NEON["magenta"])
        self._add_btn(r4, "⚡", "Smart Install (Missing)", self.smart_install, NEON["magenta"])
        ofl.addLayout(r4)
        r5 = QHBoxLayout()
        r5.setSpacing(6)
        self._add_btn(r5, "⬆️", "Update pip (Offline)", self.upgrade_pip_offline, NEON["magenta"])
        self._add_btn(r5, "🔥", "Clean Wipe", self.reset_env, NEON["red"])
        ofl.addLayout(r5)
        cmd_layout.addWidget(offline_grp)

        cmd_layout.addStretch()  # push groups to top
        splitter.addWidget(cmd_panel)

        # ── BOTTOM HALF: Progress + Terminal ──
        terminal_panel = QWidget()
        term_layout = QVBoxLayout(terminal_panel)
        term_layout.setContentsMargins(0, 4, 0, 0)
        term_layout.setSpacing(4)

        # Progress bar + percentage label
        prog_row = QHBoxLayout()
        prog_row.setSpacing(8)

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.progress.setFixedHeight(20)
        self.progress.setFormat("%p%")
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {NEON['border']};
                border-radius: 4px;
                background-color: {NEON['bg_panel']};
                text-align: center;
                color: {NEON['text']};
                font-size: 10px;
                font-family: 'Consolas', monospace;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, x2:1,
                    stop:0 {NEON['cyan']},
                    stop:0.5 {NEON['magenta']},
                    stop:1 {NEON['green']});
                border-radius: 3px;
            }}
        """)
        prog_row.addWidget(self.progress)

        self.progress_label = QLabel("")
        self.progress_label.setFixedWidth(180)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.progress_label.setStyleSheet(f"""
            font-size: 10px; color: {NEON['yellow']};
            font-family: 'Consolas', monospace;
        """)
        self.progress_label.setVisible(False)
        prog_row.addWidget(self.progress_label)

        term_layout.addLayout(prog_row)

        # Status indicator
        self.status_label = QLabel("● Ready")
        self.status_label.setFixedHeight(16)
        self.status_label.setStyleSheet(f"""
            font-size: 10px; color: {NEON['green']};
            font-family: 'Consolas', monospace; padding: 0 2px;
        """)
        term_layout.addWidget(self.status_label)

        # Terminal
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("  Terminal output will appear here...")
        self.log.setStyleSheet(f"""
            QTextEdit {{
                background-color: #06060c;
                border: 1px solid {NEON['border']};
                border-radius: 8px;
                color: {NEON['text']};
                font-family: 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                padding: 8px;
                selection-background-color: {NEON['cyan_dim']};
            }}
        """)
        term_layout.addWidget(self.log)

        splitter.addWidget(terminal_panel)

        # ── Proportions: 55% commands, 45% terminal ──
        splitter.setSizes([430, 340])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        root.addWidget(splitter, stretch=1)

        # ═══════════ FOOTER ═══════════
        footer = QLabel("PyPort v2.0  ·  Offline Python Environment Manager")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setFixedHeight(18)
        footer.setStyleSheet(f"""
            font-size: 9px; color: {NEON['text_dim']};
            letter-spacing: 2px; font-family: 'Segoe UI';
        """)
        root.addWidget(footer)

        self.setLayout(root)

        # ═══════════ GLOBAL STYLESHEET ═══════════
        self.setStyleSheet(self.styleSheet() + f"""
            QWidget {{
                background-color: {NEON['bg_dark']};
                color: {NEON['text']};
                font-family: 'Segoe UI', sans-serif;
            }}
            QToolTip {{
                background-color: {NEON['bg_panel']};
                color: {NEON['text']};
                border: 1px solid {NEON['cyan_dim']};
                border-radius: 4px;
                padding: 4px 8px; font-size: 11px;
            }}
            QScrollBar:vertical {{
                background: {NEON['bg_dark']};
                width: 6px; border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {NEON['cyan_dim']};
                border-radius: 3px; min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

    # ──────────────────────────────────────────────
    #  UI HELPERS
    # ──────────────────────────────────────────────
    def _make_group(self, title, accent):
        grp = QGroupBox(f"  {title}")
        grp.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {NEON['border']};
                border-top: 2px solid {accent};
                border-radius: 10px;
                margin-top: 12px;
                padding: 10px 8px 8px 8px;
                background-color: {NEON['bg_panel']};
                font-weight: bold;
                color: {accent};
                font-size: 10px;
                letter-spacing: 2px;
                font-family: 'Segoe UI';
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px;
                background-color: {NEON['bg_panel']};
            }}
        """)
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(6, 4, 6, 6)
        grp.setLayout(layout)
        return grp

    def _add_btn(self, layout, icon, text, func, accent):
        btn = NeonButton(icon, text, accent)
        btn.clicked.connect(func)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(btn)

    def set_status(self, text, color=None):
        color = color or NEON["cyan"]
        self.status_label.setText(f"● {text}")
        self.status_label.setStyleSheet(f"font-size: 10px; color: {color}; font-family: 'Consolas', monospace; padding: 0 2px;")

    # ──────────────────────────────────────────────
    #  PROGRESS & COMMAND
    # ──────────────────────────────────────────────
    def start_progress(self, indeterminate=False):
        self.progress.setVisible(True)
        self.progress_label.setVisible(True)
        if indeterminate:
            self.progress.setMaximum(0)
            self.progress_label.setText("⏳ Working...")
        else:
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.progress_label.setText("0%  ⏳ Starting...")
        self.set_status("Working...", NEON["yellow"])

    def stop_progress(self):
        self.progress.setMaximum(100)
        self.progress.setValue(100)
        self.progress_label.setText("100%  ✓ Complete")
        QTimer.singleShot(3000, self._hide_progress)

    def _hide_progress(self):
        self.progress.setVisible(False)
        self.progress_label.setVisible(False)
        self.progress.setValue(0)

    def _update_progress(self, pct):
        pct = min(pct, 100)
        if self.progress.maximum() == 0:
            self.progress.setMaximum(100)
        self.progress.setValue(pct)
        if pct < 30:
            self.progress_label.setText(f"{pct}%  ⏳ Starting...")
        elif pct < 70:
            self.progress_label.setText(f"{pct}%  🔄 In progress...")
        elif pct < 100:
            self.progress_label.setText(f"{pct}%  ⚡ Almost there...")
        else:
            self.progress_label.setText(f"100%  ✓ Complete")

    def run_command(self, command, success_msg=None, error_msg=None,
                    expected_lines=0, indeterminate=True):
        self.start_progress(indeterminate=indeterminate and expected_lines == 0)

        self.worker = CommandWorker(command, expected_lines)
        self.worker.output_signal.connect(self._log_output)
        self.worker.error_signal.connect(self._log_error)
        self.worker.progress_signal.connect(self._update_progress)
        self.worker.finished_status.connect(
            lambda ok: self._on_command_done(ok, success_msg, error_msg)
        )
        self.worker.finished.connect(self.stop_progress)
        self.worker.start()

    def _log_output(self, text):
        self.log.append(f'<span style="color:{NEON["text"]};">{text}</span>')

    def _log_error(self, text):
        self.log.append(f'<span style="color:{NEON["red"]};">⚠ {text}</span>')

    def _on_command_done(self, success, success_msg, error_msg):
        if success:
            self.set_status(success_msg or "Done", NEON["green"])
            if success_msg:
                self.log.append(f'<span style="color:{NEON["green"]};">✅ {success_msg}</span>')
        else:
            self.set_status("Error occurred", NEON["red"])
            if error_msg:
                self.log.append(f'<span style="color:{NEON["red"]};">❌ {error_msg}</span>')

    # ──────────────────────────────────────────────
    #  TYPEWRITER
    # ──────────────────────────────────────────────
    def typewriter_effect(self):
        if self.current_index < len(self.full_text):
            self.subtitle.setText(
                self.subtitle.text() + self.full_text[self.current_index]
            )
            self.current_index += 1
        else:
            self.type_timer.stop()

    # ══════════════════════════════════════════════
    #  COMMON
    # ══════════════════════════════════════════════
    def show_packages(self):
        self.log.clear()
        self.set_status("Loading installed modules...", NEON["cyan"])
        self.start_progress(indeterminate=False)

        pkgs = list(distributions())
        total = len(pkgs)
        count = 0

        for i, dist in enumerate(pkgs):
            if dist.metadata['Name']:
                name = dist.metadata['Name']
                ver = dist.version
                self.log.append(
                    f'<span style="color:{NEON["cyan"]};">{name}</span>'
                    f'<span style="color:{NEON["text_dim"]};">==</span>'
                    f'<span style="color:{NEON["green"]};">{ver}</span>'
                )
                count += 1
            pct = int((i + 1) / total * 100) if total else 100
            self._update_progress(pct)
            QApplication.processEvents()

        self.log.append(f'\n<span style="color:{NEON["yellow"]};">📦 Total: {count} packages</span>')
        self.set_status(f"{count} packages found", NEON["green"])
        self.stop_progress()

    def check_python_version(self):
        self.log.clear()
        self.run_command("python --version", "Python version retrieved")

    def check_pip_version(self):
        self.log.clear()
        self.run_command("pip --version", "pip version retrieved")

    def install_package(self):
        pkg = self.package_input.text().strip()
        if not pkg:
            NeonDialog.show_warning(
                self, "No Package Name",
                "Please enter a package name in the input field before clicking Install.",
                "Example:  numpy, pandas, requests"
            )
            return
        self.log.append(f'<span style="color:{NEON["cyan"]};">📥 Installing <b>{pkg}</b>...</span>')
        self.run_command(
            f"pip install {pkg}",
            success_msg=f"{pkg} installed successfully",
            error_msg=f"Failed to install {pkg}"
        )

    # ══════════════════════════════════════════════
    #  ONLINE PC
    # ══════════════════════════════════════════════
    def export_requirements(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save requirements.txt", "requirements.txt", "Text Files (*.txt)")
        if path:
            self.run_command(f'pip freeze > "{path}"', f"Exported to {os.path.basename(path)}", "Export failed")
        else:
            NeonDialog.show_info(self, "Cancelled", "Export was cancelled.")

    def download_packages(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select requirements.txt", "", "Text Files (*.txt)")
        if not file_path:
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if not folder:
            return

        try:
            with open(file_path) as f:
                line_count = sum(1 for l in f if l.strip() and "==" in l) + 3
        except Exception:
            line_count = 0

        self.log.append(f'<span style="color:{NEON["green"]};">⬇️ Downloading packages + pip/setuptools/wheel...</span>')
        self.run_command(
            f'pip download -r "{file_path}" pip setuptools wheel -d "{folder}"',
            success_msg="All packages downloaded",
            error_msg="Download encountered errors",
            expected_lines=line_count * 3
        )

    def update_pip(self):
        self.log.clear()
        self.log.append(f'<span style="color:{NEON["green"]};">⬆️ Updating pip online...</span>')
        self.run_command("python -m pip install --upgrade pip", "pip updated successfully", "pip update failed")

    def prepare_offline_kit(self):
        base_dir = QFileDialog.getExistingDirectory(self, "Select Folder for Offline Kit")
        if not base_dir:
            return

        self.kit_dir = os.path.join(base_dir, "Offline_Kit")
        self.pkg_dir = os.path.join(self.kit_dir, "packages")
        os.makedirs(self.pkg_dir, exist_ok=True)
        self.req = os.path.join(self.kit_dir, "requirements.txt")

        self.log.append(f'<span style="color:{NEON["cyan"]};">📦 Step 1/3 — Freezing requirements...</span>')
        self.start_progress(indeterminate=False)
        self._update_progress(10)

        self.worker = CommandWorker(f'pip freeze > "{self.req}"')
        self.worker.output_signal.connect(self._log_output)

        def step2():
            self._update_progress(30)
            self.log.append(f'<span style="color:{NEON["green"]};">⬇️ Step 2/3 — Downloading packages...</span>')

            self.worker2 = CommandWorker(
                f'pip download -r "{self.req}" pip setuptools wheel -d "{self.pkg_dir}"'
            )
            self.worker2.output_signal.connect(self._log_output)
            self.worker2.progress_signal.connect(
                lambda p: self._update_progress(30 + int(p * 0.5))
            )

            def step3():
                self._update_progress(85)
                self.log.append(f'<span style="color:{NEON["yellow"]};">📁 Step 3/3 — Creating zip...</span>')

                with open(os.path.join(self.kit_dir, "install.bat"), "w") as f:
                    f.write('@echo off\n')
                    f.write('echo Installing packages from Offline Kit...\n')
                    f.write('pip install --no-index --find-links=packages -r requirements.txt\n')
                    f.write('echo Upgrading pip...\n')
                    f.write('python -m pip install --no-index --find-links=packages --upgrade pip\n')
                    f.write('echo Done!\n')
                    f.write('pause\n')

                zip_path = os.path.join(base_dir, "Offline_Kit.zip")
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                    for root_dir, _, files in os.walk(self.kit_dir):
                        for file in files:
                            path = os.path.join(root_dir, file)
                            z.write(path, os.path.relpath(path, self.kit_dir))

                self.stop_progress()
                NeonDialog.show_success(
                    self, "Offline Kit Ready!",
                    "Full offline kit has been created and zipped.",
                    f"Location: {zip_path}"
                )
                self.set_status("Offline Kit created", NEON["green"])

            self.worker2.finished.connect(step3)
            self.worker2.start()

        self.worker.finished.connect(step2)
        self.worker.start()

    def smart_export(self):
        prev_file, _ = QFileDialog.getOpenFileName(self, "Select Previous requirements.txt", "", "Text Files (*.txt)")
        if not prev_file:
            NeonDialog.show_warning(self, "No File Selected", "You need to select the previous requirements.txt to compare against.")
            return

        base_dir = QFileDialog.getExistingDirectory(self, "Select Folder to Save Smart Offline Kit")
        if not base_dir:
            return

        current = {
            dist.metadata['Name']: dist.version
            for dist in distributions() if dist.metadata['Name']
        }

        previous = {}
        try:
            with open(prev_file, "r") as f:
                for line in f:
                    if "==" in line:
                        name, version = line.strip().split("==", 1)
                        previous[name] = version
        except Exception as e:
            NeonDialog.show_error(self, "File Read Error", "Could not read the previous requirements file.", str(e))
            return

        new_packages = [f"{n}=={v}" for n, v in current.items() if n not in previous]

        if not new_packages:
            NeonDialog.show_info(self, "All Synced", "No new packages found. Your environments are already in sync!")
            return

        self.log.append(f'<span style="color:{NEON["yellow"]};">📦 Found {len(new_packages)} new packages</span>')

        kit_dir = os.path.join(base_dir, "Smart_Offline_Kit")
        pkg_dir = os.path.join(kit_dir, "packages")
        os.makedirs(pkg_dir, exist_ok=True)

        req_file = os.path.join(kit_dir, "requirements.txt")
        with open(req_file, "w") as f:
            f.write("\n".join(new_packages))

        self.log.append(f'<span style="color:{NEON["green"]};">⬇️ Downloading new packages...</span>')
        self.start_progress(indeterminate=False)
        self._update_progress(10)

        self.worker = CommandWorker(
            f'pip download {" ".join(new_packages)} -d "{pkg_dir}"',
            expected_lines=len(new_packages) * 3
        )
        self.worker.output_signal.connect(self._log_output)
        self.worker.error_signal.connect(self._log_error)
        self.worker.progress_signal.connect(
            lambda p: self._update_progress(10 + int(p * 0.7))
        )

        def on_done():
            self._update_progress(85)

            with open(os.path.join(kit_dir, "install.bat"), "w") as f:
                f.write("@echo off\n")
                f.write("echo Installing NEW packages only...\n")
                f.write("pip install --no-index --find-links=packages -r requirements.txt\n")
                f.write("echo Done!\n")
                f.write("pause\n")

            zip_path = os.path.join(base_dir, "Smart_Offline_Kit.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root_dir, dirs, files in os.walk(kit_dir):
                    for file in files:
                        full_path = os.path.join(root_dir, file)
                        arcname = os.path.relpath(full_path, kit_dir)
                        zipf.write(full_path, arcname)

            self.stop_progress()
            NeonDialog.show_success(
                self, "Smart Kit Ready!",
                f"Created kit with {len(new_packages)} new packages.",
                f"Location: {zip_path}"
            )
            self.set_status("Smart Offline Kit created", NEON["green"])

        self.worker.finished.connect(on_done)
        self.worker.start()

    # ══════════════════════════════════════════════
    #  OFFLINE PC
    # ══════════════════════════════════════════════
    def install_from_folder(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select requirements.txt", "", "Text Files (*.txt)")
        if not file_path:
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Packages Folder")
        if not folder:
            return

        try:
            with open(file_path) as f:
                lc = sum(1 for l in f if l.strip())
        except Exception:
            lc = 0

        self.log.append(f'<span style="color:{NEON["magenta"]};">📥 Installing from offline folder...</span>')
        self.run_command(
            f'pip install --no-index --find-links="{folder}" -r "{file_path}"',
            success_msg="Offline installation complete",
            error_msg="Offline installation encountered errors",
            expected_lines=lc * 2
        )

    def smart_install(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select requirements.txt", "", "Text Files (*.txt)")
        if not file_path:
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Packages Folder")
        if not folder:
            return

        installed = {d.metadata['Name'].lower() for d in distributions() if d.metadata['Name']}

        needed = []
        for line in open(file_path):
            if "==" in line:
                name = line.split("==")[0]
                if name.lower() not in installed:
                    needed.append(line.strip())

        if not needed:
            NeonDialog.show_info(self, "All Caught Up!", "Every package is already installed. Nothing to do.")
            self.set_status("All packages installed", NEON["green"])
            return

        self.log.append(f'<span style="color:{NEON["magenta"]};">⚡ Installing {len(needed)} missing packages...</span>')
        self.run_command(
            f'pip install --no-index --find-links="{folder}" {" ".join(needed)}',
            success_msg=f"{len(needed)} packages installed",
            error_msg="Smart install encountered errors",
            expected_lines=len(needed) * 2
        )

    def upgrade_pip_offline(self):
        NeonDialog.show_info(
            self, "Heads Up!",
            "Make sure the selected folder contains the pip .whl file.\n\n"
            "This file should have been downloaded via 'Download Packages' or "
            "'Full Offline Kit' on your Online PC.",
            "If you used 'Smart Export', pip won't be included since it was already "
            "installed. Re-download using 'Download Packages' to get the pip wheel."
        )

        folder = QFileDialog.getExistingDirectory(self, "Select Folder with pip Wheel File")
        if not folder:
            return

        pip_found = any(f.startswith("pip-") and f.endswith(".whl") for f in os.listdir(folder))

        if not pip_found:
            NeonDialog.show_error(
                self, "pip Wheel Not Found",
                "No pip .whl file found in the selected folder!",
                "Go to your Online PC → use 'Download Packages' or 'Full Offline Kit' "
                "to download the pip wheel, then transfer that folder here."
            )
            return

        self.log.append(f'<span style="color:{NEON["magenta"]};">⬆️ Upgrading pip from offline wheel...</span>')
        self.run_command(
            f'python -m pip install --no-index --find-links="{folder}" --upgrade pip',
            success_msg="pip upgraded successfully",
            error_msg="pip upgrade failed — check the log for details"
        )

    def reset_env(self):
        if self.package_input.text().strip() != "CONFIRM":
            NeonDialog.show_warning(
                self, "Confirmation Required",
                "This will uninstall ALL packages except pip, setuptools, and wheel.",
                "Type CONFIRM in the input field and click 'Clean Wipe' again."
            )
            return

        confirmed = NeonDialog.ask_confirm(
            self, "🔥 Nuclear Option",
            "You're about to wipe ALL installed packages.\nThis cannot be undone. Are you absolutely sure?",
            "pip, setuptools, and wheel will be preserved."
        )
        if not confirmed:
            self.set_status("Wipe cancelled", NEON["yellow"])
            return

        pkgs = [
            d.metadata['Name'] for d in distributions()
            if d.metadata['Name'] and d.metadata['Name'].lower() not in ["pip", "setuptools", "wheel"]
        ]

        if not pkgs:
            NeonDialog.show_info(self, "Already Clean", "No packages to remove — environment is already clean.")
            return

        self.log.append(f'<span style="color:{NEON["red"]};">🔥 Wiping {len(pkgs)} packages...</span>')
        self.run_command(
            f"pip uninstall -y {' '.join(pkgs)}",
            success_msg="Environment wiped clean",
            error_msg="Some packages could not be removed",
            expected_lines=len(pkgs)
        )


# ══════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(create_app_icon())
    app.setStyle("Fusion")
    window = PackageManager()
    window.show()
    sys.exit(app.exec())
