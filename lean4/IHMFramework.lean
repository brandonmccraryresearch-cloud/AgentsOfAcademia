-- This module serves as the root of the `IHMFramework` library.
-- Import modules here that should be built as part of the library.
--
-- IMPORTANT — naming-conflict guard:
--   `IHMFramework.Basic` defines `latticeSpacing` and `d4CoordinationNumber`.
--   `IHMFramework.Circularity` imports Basic and must NOT redefine these names.
--   `IHMFramework.FiveDesign` imports Basic and must NOT redefine `d4CoordinationNumber`.
--   Violating this constraint causes "environment already contains 'X'" errors.
import IHMFramework.Basic
import IHMFramework.V2Basic
import IHMFramework.V2Problems
import IHMFramework.FiveDesign
import IHMFramework.Circularity
-- Tier 4 Lean 4 Formalization (Session 8)
import IHMFramework.LiebRobinson
import IHMFramework.MeasureUniqueness
import IHMFramework.D4Uniqueness
import IHMFramework.Goldstone
import IHMFramework.GaugeInvariance
-- v84.0 additions
import IHMFramework.ReggeContinuumLimit
-- v85.0 additions
import IHMFramework.NonAbelianGauge
-- v86.0 additions (Session 18)
import IHMFramework.DiracEquation
import IHMFramework.BornRule
import IHMFramework.ModeDecomposition
-- Lorentzian signature + Koide triality formalizations
import IHMFramework.LorentzianSignature
import IHMFramework.KoideTriality
-- Formal Verification Registry (public registry table + stub axioms)
import IHMFramework.FormalVerificationRegistry
