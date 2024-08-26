from app.DORApy.classes.modules.connect_path import s3,s3r
from flask import jsonify, request
import jwt
import bcrypt
import os
import sys
import pandas as pd
import py7zr
import io

SECRET_JKEY = os.getenv('SECRET_JKEY')
environment = os.getenv('ENVIRONMENT')
bucket_common_files = os.getenv('S3_BUCKET_COMMON_FILES')
bucket_users_files = os.getenv('S3_BUCKET_USERS_FILES')
s3_region = os.getenv('S3_UPLOADS_REGION')
s3_access_key = os.getenv('S3_UPLOADS_ACCESS_KEY')
s3_secret_key = os.getenv('S3_UPLOADS_SECRET_KEY')


#dict_dict_info_REF = DictDfInfoShp({})
#dict_dict_info_REF = dict_dict_info_REF.creation_DictDfInfoShp(['MO'])

if environment=="developpement":
    chemin_vers_file = "app/files/"
if environment=="docker":
    chemin_vers_file = "files/"

def upload_df_to_s3(df, bucket_common_files, file_key):
    s3_path = f's3://{bucket_common_files}/{file_key}'
    df.to_csv(s3_path, index=False, storage_options={'anon': False})

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def import_dict_users_s3():
    file_name = "BDD_users/db_users.csv"
    csv_obj = s3.get_object(Bucket=bucket_users_files,Key=file_name)
    csv_content = csv_obj['Body'].read().decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_content))
    dict_users = df.set_index('email').to_dict(orient='index')
    return dict_users

def hash_mdp_s3():
    file_name = "BDD_users/db_users.csv"
    csv_obj = s3.get_object(Bucket="dorabuckets3",Key=file_name)
    csv_content = csv_obj['Body'].read().decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_content))
    df["password"] = df["password"].apply(lambda x: hash_password(x))
    upload_df_to_s3(df, bucket_users_files, file_name)

def check_token(token):
    if not token:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        decoded_token = jwt.decode(token, SECRET_JKEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403   
    return decoded_token

'''def synchro_files_vm_avec_s3():
    def DL_et_unzip_optionnel(raison_du_dl,chemin,nom_fichier):
        s3.download_file(bucket_common_files,file.key, os.path.join("./", chemin_vers_file, chemin,nom_fichier))
        print("J'ai dl le fichier " + raison_du_dl + " suivant : " + file.key)
        dict_date_7z_sur_EC2[file.key] = date_modification_sur_s3
        archive = py7zr.SevenZipFile(os.path.join("./", chemin_vers_file, chemin,nom_fichier), mode='r')
        archive.extractall(path=os.path.join("./", chemin_vers_file, chemin))
        archive.close()
        return dict_date_7z_sur_EC2

    list_dossier_a_synchro_du_s3 = ['shp_files']
    list_fichiers_a_traiter = ['CT.7z']

    for nom_dossier in list_dossier_a_synchro_du_s3:
    #list_fichiers_dossier_files_s3 = glob.glob(chemin_fichier_tableau + "/*." + type_fichier)
        if os.path.isfile(os.path.join("./", chemin_vers_file,"date_modif_par_7z.csv")):
            df_csv = pd.read_csv(os.path.join("./", chemin_vers_file,"date_modif_par_7z.csv"))
            dict_date_7z_sur_EC2 = dict(zip(df_csv['nom'], df_csv['date']))
            dict_7z_s3bucker_shp_files = bucket_common_files.objects.all()
            dict_date_s3 = {}
            for file in dict_7z_s3bucker_shp_files:
                if file.get()['ContentType'].split(";")[0] != 'application/x-directory':
                    nom_dossier_maitre = file.key.split("/")[0]
                    nom_fichier = file.key.split("/")[-1]
                    chemin = "/".join(file.key.split("/")[:-1])+'/'
                    if nom_fichier in list_fichiers_a_traiter:
                        if nom_dossier_maitre in list_dossier_a_synchro_du_s3:
                            date_modification_sur_s3 = s3.head_object(Bucket=bucket_common_files, Key=file.key)['LastModified']
                            if file.key in list(dict_date_7z_sur_EC2):
                                raison_du_dl = "outdated"
                                if dict_date_7z_sur_EC2[file.key]!=date_modification_sur_s3.strftime("%Y-%m-%d %H:%M:%S+00:00"):
                                    dict_date_7z_sur_EC2 = DL_et_unzip_optionnel(raison_du_dl,chemin,nom_fichier)
                            if file.key not in list(dict_date_7z_sur_EC2):
                                if not os.path.exists(os.path.join("./", chemin_vers_file, chemin)):
                                    os.makedirs(os.path.join("./", chemin_vers_file, chemin))
                                raison_du_dl = "inconnu"
                                dict_date_7z_sur_EC2 = DL_et_unzip_optionnel(raison_du_dl,chemin,nom_fichier)


    df_date_7z_sur_EC2 = pd.DataFrame.from_dict(dict_date_7z_sur_EC2.items())                  
    df_date_7z_sur_EC2.columns = ['nom','date']
    df_date_7z_sur_EC2.to_csv(os.path.join("./", chemin_vers_file,"date_modif_par_7z.csv"), index=False)

def actualisation_dossier_MO():
    dossier_user_MO_gemapi = "app\\MO_gemapi"
    list_rep_MO_gemapi = Class_Folder.lister_rep_et_fichiers(dossier_user_MO_gemapi)
    list_NOM_rep = [REP.name for REP in list_rep_MO_gemapi]

    liste_CODE_MO_totaux = dict_dict_info_REF['df_info_MO'].loc[dict_dict_info_REF['df_info_MO']['CODE_DEP']=="33"]['CODE_MO'].to_list()
    list_repertoire_manquant = [k for k in liste_CODE_MO_totaux if k not in list_NOM_rep]
    for NOM_REP in list_repertoire_manquant:
        if NOM_REP not in list_NOM_rep:
            if environment=="docker":
                dossier_user_MO_gemapi = dossier_user_MO_gemapi.replace("\\","/")
                os.mkdir(os.path.join("/",dossier_user_MO_gemapi,NOM_REP))
            if environment=="developpement":
                os.mkdir(os.path.join(dossier_user_MO_gemapi,NOM_REP))
        if NOM_REP in list_NOM_rep:
            print("probleme avec le syndicat : " + NOM_REP, file=sys.stderr)'''

    

