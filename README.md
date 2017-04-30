# um-ab-mspdata
(ArcGIS Python Script Tool)

Merges multiple feature classes of any shape types into three feature classes of shape types: point / polygon / polyline. Suffixes "_point", "_polygon" or "_polyline" will be added to the basename chosen by the user.

Output feature classes contain only following fields:
* seaUse
* useType
* useDsc
* srcLayer
* srcPath

Preserves already existing values in srcLayer and serPath fields.

