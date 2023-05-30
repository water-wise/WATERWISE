from sklearn.base import BaseEstimator, TransformerMixin

class CatImputer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        
        self.thermal_design = X[X.process=='Thermal'].thermal_design.mode()[0]
        self.ro_system = X[X.technology=='ro (reverse osmosis)'].ro_system.mode()[0]
        self.ro_membrane_type = X[X.technology=='ro (reverse osmosis)'].ro_membrane_type.mode()[0]
        
        self.general_imputer = X.mode().iloc[0].to_dict()
        
        return self

    def transform(self, X):
        df = X.copy()
        
        df.loc[(df.process=='Thermal')&(df.thermal_design.isna()),'thermal_design']=self.thermal_design
        df.loc[(df.technology=='ro (reverse osmosis)')&(df.ro_system.isna()),'ro_system']=self.ro_system
        df.loc[(df.technology=='ro (reverse osmosis)')&(df.ro_membrane_type.isna()),'ro_membrane_type']=self.ro_membrane_type
        df.loc[:,['thermal_design','ro_system','ro_membrane_type']]=df[['thermal_design','ro_system','ro_membrane_type']].fillna('N/A')

        df.fillna(self.general_imputer,inplace=True)    
        return df