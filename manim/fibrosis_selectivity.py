"""
Manim scene: "Target selectivity isn't the lever — tissue localization is."

Animates the core insight behind the Anti-Fibrotic Placeholder Drug Designer:
  1. A promiscuous drug hits many genes -> many harms.
  2. Making it *selective* removes OFF-TARGET harms.
  3. But the worst harms are the RIGHT target in the WRONG tissue -> selectivity
     cannot remove them.
  4. The real lever is LOCALIZATION (where the drug is allowed to act).

Renders with Manim Community Edition (no LaTeX required -- uses Text only).

    pip install manim
    manim -qm fibrosis_selectivity.py FibrosisSelectivity      # 720p
    manim -qh fibrosis_selectivity.py FibrosisSelectivity      # 1080p
    manim -qh --format=gif fibrosis_selectivity.py FibrosisSelectivity

Author: Glen Ritschel
License: MIT
"""

from manim import *

# palette (matches the web tool)
INK   = "#e8edf3"
MUTED = "#9aa6b2"
WANT  = "#4da6e0"   # therapeutic target
OFF   = "#e08a5a"   # off-target
GOOD  = "#51cf66"   # benefit / efficacy
BAD   = "#e56b62"   # serious adverse effect
WARN  = "#f0c15a"   # moderate adverse effect
CARD  = "#232c38"
STROKE= "#39424f"

config.background_color = "#11161d"


def node(label, color=INK, w=2.4, h=0.7, fill=CARD, fs=26):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                           fill_color=fill, fill_opacity=1.0,
                           stroke_color=color, stroke_width=2.5)
    txt = Text(label, font_size=fs, color=INK).move_to(box.get_center())
    if txt.width > w - 0.3:
        txt.scale((w - 0.3) / txt.width)
    return VGroup(box, txt)


def edge(a, b, color=MUTED, width=4, tip=True):
    start = a.get_right() + RIGHT * 0.03
    end = b.get_left() + LEFT * 0.03
    if tip:
        return Arrow(start, end, buff=0.08, color=color, stroke_width=width,
                     max_tip_length_to_length_ratio=0.08)
    return Line(start, end, color=color, stroke_width=width)


class FibrosisSelectivity(Scene):
    def construct(self):
        self.title_card()
        self.promiscuous()
        self.make_selective()
        self.wrong_tissue()
        self.localization()
        self.closing()

    # ---------------------------------------------------------------
    def title_card(self):
        t1 = Text("A more selective drug", font_size=52, color=INK)
        t2 = Text("won't fix fibrosis.", font_size=52, color=INK, weight=BOLD)
        grp = VGroup(t1, t2).arrange(DOWN, buff=0.22)
        sub = Text("on-target  ≠  off-tissue", font_size=30, color=MUTED)
        sub.next_to(grp, DOWN, buff=0.6)
        self.play(Write(grp), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.9)
        self.wait(1.4)
        self.play(FadeOut(grp), FadeOut(sub), run_time=0.7)

    # ---------------------------------------------------------------
    def promiscuous(self):
        drug = node("Drug", color=WANT, w=1.8, h=0.9, fs=30).to_edge(LEFT, buff=0.7)

        # targets
        src = node("SRC", color=WANT, w=1.6, h=0.6)
        mek = node("MEK", color=WANT, w=1.6, h=0.6)
        kit = node("KIT", color=OFF, w=1.6, h=0.6)
        herg = node("hERG", color=OFF, w=1.6, h=0.6)
        btk = node("BTK", color=OFF, w=1.6, h=0.6)
        targets = VGroup(src, mek, kit, herg, btk).arrange(DOWN, buff=0.28)
        targets.move_to(LEFT * 1.2)

        # outcomes
        rev = node("Fibrosis reversal", color=GOOD, w=3.0, h=0.6, fs=22)
        pah = node("PAH", color=BAD, w=2.2, h=0.55, fs=22)
        cyto = node("Cytopenias", color=BAD, w=2.2, h=0.55, fs=22)
        qt = node("QT prolong.", color=BAD, w=2.2, h=0.55, fs=22)
        bleed = node("Bleeding", color=BAD, w=2.2, h=0.55, fs=22)
        rash = node("Rash", color=WARN, w=2.2, h=0.55, fs=22)
        outs = VGroup(rev, pah, cyto, qt, bleed, rash).arrange(DOWN, buff=0.22)
        outs.to_edge(RIGHT, buff=0.7)

        self.drug, self.src, self.mek = drug, src, mek
        self.kit, self.herg, self.btk = kit, herg, btk
        self.rev, self.pah, self.cyto, self.qt, self.bleed, self.rash = rev, pah, cyto, qt, bleed, rash

        # edges drug->targets
        d_edges = VGroup(*[edge(drug, t, color=(WANT if t in (src, mek) else OFF), width=3)
                           for t in (src, mek, kit, herg, btk)])
        # target->outcome edges
        e_src_rev = edge(src, rev, color=GOOD)
        e_src_pah = edge(src, pah, color=BAD)
        e_mek_rev = edge(mek, rev, color=GOOD)
        e_mek_rash = edge(mek, rash, color=WARN)
        e_kit = edge(kit, cyto, color=BAD)
        e_herg = edge(herg, qt, color=BAD)
        e_btk = edge(btk, bleed, color=BAD)
        self.off_edges = VGroup(e_kit, e_herg, e_btk)
        self.off_targets = VGroup(kit, herg, btk)
        self.off_outs = VGroup(cyto, qt, bleed)
        self.d_off_edges = VGroup(d_edges[2], d_edges[3], d_edges[4])
        self.src_pah_edge = e_src_pah

        caption = Text("Promiscuous drug → many harms", font_size=28, color=MUTED).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(drug), run_time=0.5)
        self.play(LaggedStart(*[Create(e) for e in d_edges], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(t) for t in targets], lag_ratio=0.15), run_time=1.4)
        self.play(LaggedStart(Create(e_src_rev), Create(e_mek_rev), Create(e_src_pah),
                              Create(e_mek_rash), Create(e_kit), Create(e_herg), Create(e_btk),
                              lag_ratio=0.12),
                  LaggedStart(FadeIn(rev), FadeIn(pah), FadeIn(rash), FadeIn(cyto), FadeIn(qt), FadeIn(bleed),
                              lag_ratio=0.12), run_time=1.8)
        self.play(FadeIn(caption, shift=UP * 0.2))
        self.caption = caption
        self.wait(1.2)

    # ---------------------------------------------------------------
    def make_selective(self):
        new_cap = Text("Make it selective → off-target harms gone ✓",
                       font_size=28, color=GOOD).to_edge(DOWN, buff=0.4)
        self.play(Transform(self.caption, new_cap), run_time=0.6)
        self.play(FadeOut(self.off_targets), FadeOut(self.off_outs),
                  FadeOut(self.off_edges), FadeOut(self.d_off_edges), run_time=1.2)
        self.wait(1.0)

    # ---------------------------------------------------------------
    def wrong_tissue(self):
        new_cap = Text("But the worst ones remain", font_size=28, color=BAD).to_edge(DOWN, buff=0.4)
        self.play(Transform(self.caption, new_cap), run_time=0.6)

        # relabel outcome tissues for SRC
        rev_t = Text("Fibrosis reversal\n(myofibroblast)", font_size=20, color=INK,
                     line_spacing=0.7).move_to(self.rev[1].get_center())
        pah_t = Text("PAH\n(lung vessels)", font_size=20, color=INK,
                     line_spacing=0.7).move_to(self.pah[1].get_center())
        self.play(Transform(self.rev[1], rev_t), Transform(self.pah[1], pah_t), run_time=0.6)

        box = SurroundingRectangle(self.src, color=WARN, buff=0.12, stroke_width=4)
        lbl = Text("same target", font_size=22, color=WARN).next_to(box, UP, buff=0.15)
        self.play(Create(box), FadeIn(lbl), run_time=0.7)
        self.play(Indicate(self.src, color=WARN, scale_factor=1.15), run_time=0.8)
        self.play(self.src_pah_edge.animate.set_stroke(width=8), run_time=0.5)
        self.play(Flash(self.pah, color=BAD, flash_radius=1.4), run_time=0.8)

        msg = Text("Right tissue vs wrong tissue — selectivity can't tell them apart",
                   font_size=24, color=INK)
        msg.next_to(self.caption, UP, buff=0.25)
        self.play(FadeIn(msg, shift=UP * 0.2), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(msg), FadeOut(box), FadeOut(lbl), run_time=0.6)
        self.src_box = None

    # ---------------------------------------------------------------
    def localization(self):
        new_cap = Text("The real lever: localization", font_size=30, color=GOOD, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(Transform(self.caption, new_cap), run_time=0.6)

        deliver = SurroundingRectangle(self.drug, color=GOOD, buff=0.18, stroke_width=4, corner_radius=0.12)
        dlabel = Text("deliver to\nfibrotic tissue only", font_size=20, color=GOOD,
                      line_spacing=0.7).next_to(deliver, UP, buff=0.2)
        self.play(Create(deliver), FadeIn(dlabel), run_time=0.9)

        # off-tissue harms fade: PAH, rash (mek off-tissue), and their edges
        self.play(FadeOut(self.pah), FadeOut(self.src_pah_edge),
                  FadeOut(self.rash), run_time=1.2)
        # highlight surviving efficacy
        self.play(Indicate(self.rev, color=GOOD, scale_factor=1.12), run_time=0.9)

        msg = Text("Restrict where it acts → off-tissue harms vanish, efficacy stays",
                   font_size=24, color=GOOD)
        msg.next_to(self.caption, UP, buff=0.25)
        self.play(FadeIn(msg, shift=UP * 0.2), run_time=0.8)
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ---------------------------------------------------------------
    def closing(self):
        l1 = Text("Target selectivity isn't the lever.", font_size=40, color=INK)
        l2 = Text("Tissue localization is.", font_size=44, color=GOOD, weight=BOLD)
        grp = VGroup(l1, l2).arrange(DOWN, buff=0.28)
        self.play(Write(grp), run_time=1.6)
        cta = Text("interactive tool + open source  →  github.com/<your-handle>/fibrosis-drug-designer",
                   font_size=24, color=MUTED)
        cta.next_to(grp, DOWN, buff=0.7)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(grp), FadeOut(cta), run_time=0.8)
