#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creates a button"""

# Part of the PsychoPy library
# Copyright (C) 2018 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

from __future__ import absolute_import, print_function
from psychopy import visual, event
from psychopy.visual.shape import BaseShapeStim

__author__ = 'Anthony Haffey'

class ButtonStim(BaseShapeStim):
    """A class for putting a button into your experiment.

    """

    def __init__(self,
                 win,
                 borderThickness=.003,
                 labelSize=0.03,
                 pos=(0, 0),
                 labelText="text for button",
                 textColor='blue',
                 borderColor='blue',
                 buttonColor='white',
                 ):

        # local variables
        super(ButtonStim, self).__init__(win)
        button_width = len(labelText) * .025
        button_x_inner_margin = .02
        button_x_outer_margin = button_x_inner_margin + borderThickness
        button_y_inner_margin = labelSize
        button_y_outer_margin = labelSize + borderThickness
        button_x_range = (0 - button_width / 2 + pos[0], 0 + button_width / 2 + pos[0])

        self.win = win
        self.borderThickness = borderThickness
        self.labelSize = labelSize
        self.pos = pos
        self.labelText = labelText
        self.textColor = textColor
        self.borderColor = borderColor
        self.buttonColor = buttonColor

        self._dragging = False
        self.mouse = event.Mouse()
        self.buttonSelected = False
        self.buttonItems = []

        self.buttonBorder = BaseShapeStim(self.win, fillColor=self.borderColor, vertices=((button_x_range[0] - button_x_outer_margin, -button_y_outer_margin + self.pos[1]),
                                                                           (button_x_range[0] - button_x_outer_margin, button_y_outer_margin + self.pos[1]),
                                                                           (button_x_range[1] + button_x_outer_margin, button_y_outer_margin + self.pos[1]),
                                                                           (button_x_range[1] + button_x_outer_margin, -button_y_outer_margin + self.pos[1])))
        self.buttonInner = BaseShapeStim(self.win, fillColor=self.buttonColor, vertices=((button_x_range[0] - button_x_inner_margin, -button_y_inner_margin + self.pos[1]),
                                                                           (button_x_range[0] - button_x_inner_margin, button_y_inner_margin + self.pos[1]),
                                                                           (button_x_range[1] + button_x_inner_margin, button_y_inner_margin + self.pos[1]),
                                                                           (button_x_range[1] + button_x_inner_margin, -button_y_inner_margin + self.pos[1])))
        self.buttonInnerText = visual.TextStim(self.win, text=self.textColor, color=self.textColor, pos=self.pos, height=self.labelSize)
        self.buttonItems.append(self.buttonBorder)
        self.buttonItems.append(self.buttonInner)
        self.buttonItems.append(self.buttonInnerText)

    def draw(self):
        self.getMouseResponses()
        for item in self.buttonItems:
            item.draw()

    def buttonSwitch(self, switch):
        if switch:
            self.buttonBorder.color = self.buttonColor
            self.buttonInner.color = self.borderColor
            self.buttonInnerText.color = self.buttonColor
        else:
            self.buttonBorder.color = self.borderColor
            self.buttonInner.color = self.buttonColor
            self.buttonInnerText.color = self.borderColor

    def buttonContains(self, mouse):
        return self.buttonBorder.contains(mouse)

    def buttonClicked(self, mouse):
        self.buttonSelected = bool(self.buttonContains(mouse)
                                   and mouse.getPressed()[0])
        return self.buttonSelected

    def buttonGuard(self, condition):
        if condition:
            self.buttonColor = "red"

    def getMouseResponses(self):
        if not self.buttonClicked(self.mouse):  # hovering
            self.buttonSwitch(self.buttonContains(self.mouse))

        if self.buttonClicked(self.mouse):
            self._dragging = True
            # Update current but don't set Rating (mouse is still down)
            # Dragging has to start inside a "valid" area (i.e., on the
            # slider), but may continue even if the mouse moves away from
            # the slider, as long as the mouse button is not released.
        else:  # mouse is up - check if it *just* came up
            if self._dragging:
                if self.buttonContains(self.mouse):
                    self.buttonGuard(True)
                self._dragging = False
            else:
                # is up and was already up - move along
                return None

if __name__ == "__main__":
    win = visual.Window(units='height', allowStencil=True)
    button1 = ButtonStim(win, pos=(.3, -.3))
    button2 = ButtonStim(win, pos=(-.3, -.3))

    for n in range(600):
        button1.draw()
        button2.draw()
        win.flip()